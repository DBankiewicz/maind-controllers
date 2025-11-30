import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response, status, BackgroundTasks, UploadFile, Request, Form, File
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import update

import json

# Imports from your project structure
from backend.ai_core.llm_api.api import get_rag_response, get_timeline_changes, retirve_context_data_id
from database.models import User, Email, Group, EmailAnalysis
from backend.schemas import EmailIn, EmailOut, EmailAnalysisSchema, EmailWithAnalysis
from backend.dependencies import get_db, get_current_user

from backend.ai_core.data_loader.load_data import process_mail
from database.db import SessionLocal 
from database.chroma_db import collection_mails, collection_summary_mails 

from typing import List, Dict, Any
import uuid

router = APIRouter(
    tags=["Email Operations"],
    prefix='/email'
)

def analyze_emails_task(emails_data: List[Dict[str, Any]], group_id: str):
    with SessionLocal() as session:
        group = session.query(Group).where(Group.public_id==group_id).first()
        for email in emails_data:
            email_id = email['id']
            content = email['content']

            try:
                result = process_mail(content)
                public_id = str(uuid.uuid4())
                db_analysis = EmailAnalysis(
                    public_id=public_id,
                    sender=result.sender,
                    recipients=result.recipients,
                    topic=result.topic,
                    timestamp=result.timestamp,
                    summary=result.summary,
                    extra=result.extra
                )
                session.add(db_analysis)

                session.flush()

                stmt = (
                    update(Email)
                    .where(Email.id==email_id)
                    .values(analysis_id=db_analysis.id)
                )
                session.execute(stmt)
                session.commit()

                collection_mails.add(
                    ids=[str(db_analysis.id)],    
                    documents=[content] ,
                    metadatas=[{
                        "public_id": public_id,
                        "topic": result.topic
                    }],
                    # embeddings=[embedding]   # TODO custom not default  Chroma embed
                )
                if result.summary:
                    collection_summary_mails.add(
                        ids=[str(db_analysis.id)],               
                        metadatas=[{
                            "public_id": public_id,
                            "topic": result.topic
                        }],
                        documents=[result.summary]
                        # embeddings=[embedding]   # TODO custom not default  Chroma embed
                    )


            except Exception as e:
                print(e)
                session.rollback()
                continue
        group.status = "Finished"
        session.add(group)
        session.commit()
        

async def parse_final_content(file_binary: bytes) -> str:
    try:
        return file_binary.decode('utf-8')
    except Exception:
        # Fallback for non-text files or encoding errors
        return "[Error: Binary file could not be parsed]"

@router.post('', status_code=status.HTTP_202_ACCEPTED)
async def add_and_analyze(
                    request: Request,
                    background_tasks: BackgroundTasks,
                    current_user: User = Depends(get_current_user),
                    session: Session = Depends(get_db)):
    
    form_data = await request.form()
    print(form_data)
    group_id = form_data.get('group_id')
    emails_json_str = form_data.get('emails')
    attachments = form_data.getlist("attachments")
    file_map = {file.filename: file for file in attachments}

    emails = json.loads(emails_json_str)
    print(emails)
    group = session.query(Group).where(Group.public_id==group_id).first()
    if not group:
        raise HTTPException(404, detail="No group with such id")
    
    if group.user_id != current_user.id:
        raise HTTPException(401, detail="You are not authorized to add emails to this group.")
    

    new_emails = []
    for item in emails:
        content = item.get('text')
        if not content:
            file_binary = file_map.get(item.get('file_key'))

            if not file_binary:
                raise HTTPException(400, "No content nor file attached for one of emails")
            
            file_binary = await file_binary.read()
            content = await parse_final_content(file_binary)

        
        new_emails.append(Email(
            public_id=item.get('id'),
            content=content,
            group_id=group.id,
            user_id=current_user.id,
            
        ))

    group.status = "Working"
    session.add_all(new_emails)
    session.add(group)
    session.commit()

    for email in new_emails:
        session.refresh(email)

    email_payload =  [{"id": e.id, "content": e.content} for e in new_emails]

    background_tasks.add_task(analyze_emails_task, email_payload, group.public_id)


    return {"message": f"Added {len(new_emails)} emails to group {group_id}"}


@router.get('/{email_id}')
async def get_timeline_backlog(email_id: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    def get_all_emails(email_ids):
        emails = session.query(Email).options(joinedload(Email.analysis)).where(Email.public_id.in_(email_ids)).all()
        res = []
        for email in emails:
            analysis = email.analysis
            try:
                analysis=EmailAnalysisSchema(
                    sender=analysis.sender,
                    recipients=analysis.recipients,
                    topic=analysis.topic,
                    summary=analysis.summary,
                    timestamp=analysis.timestamp,
                    extra=analysis.extra
                )
            except:
                analysis=None
                
            res.append(EmailWithAnalysis(
                email_raw=EmailOut(
                    id=email.public_id,
                    text=email.content
                ),
                analysis=analysis
            ))
        
        return res

    email: EmailWithAnalysis = get_all_emails([email_id])[0]
    email_ids = retirve_context_data_id(email.email_raw.text, collection_mails, 15, 5 )
    emails = get_all_emails(email_ids) + [email] 
    output = await get_timeline_changes(emails)
    return {"message": output}

@router.post('/answer/{email_id}')
def answer_with_rag(query : str, email_id: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    def get_all_emails(email_ids):
        emails = session.query(Email).options(joinedload(Email.analysis)).where(Email.public_id.in_(email_ids)).all()
        res = []
        for email in emails:
            analysis = email.analysis
            try:
                analysis=EmailAnalysisSchema(
                    sender=analysis.sender,
                    recipients=analysis.recipients,
                    topic=analysis.topic,
                    summary=analysis.summary,
                    timestamp=analysis.timestamp,
                    extra=analysis.extra
                )
            except:
                analysis=None
                
            res.append(EmailWithAnalysis(
                email_raw=EmailOut(
                    id=email.public_id,
                    text=email.content
                ),
                analysis=analysis
            ))
        
        return res
    email: EmailWithAnalysis = get_all_emails([email_id])[0]

    final_response, context_data = get_rag_response(query, collection_mails, 5, 3)
    res = {"id": email.email_raw.id, "response": final_response, "context_data": context_data}
    return res
