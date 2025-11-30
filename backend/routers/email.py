import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response, status, BackgroundTasks, UploadFile, Request, Form, File
from pydantic import Json
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import update

# Imports from your project structure
from database.models import User, Email, Group, EmailAnalysis
from backend.schemas import EmailIn
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

def analyze_emails_task(emails_data: List[Dict[str, Any]]):
    with SessionLocal() as session:

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


            except:
                session.rollback()
                continue
        

async def parse_final_content(file_binary: bytes) -> str:
    try:
        return file_binary.decode('utf-8')
    except Exception:
        # Fallback for non-text files or encoding errors
        return "[Error: Binary file could not be parsed]"

@router.post('', status_code=status.HTTP_202_ACCEPTED)
async def add_and_analyze(
                    request: Request,
                    current_user: User = Depends(get_current_user),
                    session: Session = Depends(get_db)):
    
    form_data = await request.form()
    print(form_data)
    group_id = form_data.get('group_id')
    emails = form_data.get('emails')

    group = session.query(Group).where(Group.public_id==group_id).first()
    if not group:
        raise HTTPException(404, detail="No group with such id")
    
    if group.user_id != current_user.id:
        raise HTTPException(401, detail="You are not authorized to add emails to this group.")
    

    new_emails = []
    for item in emails:
        content = item.get('text')
        if not content:
            file_binary = form_data.get(item.get('file_key'))

            if not file_binary:
                raise HTTPException(400, "No content nor file attached for one of emails")
            
            file_binary = await file_binary.read()
            content = await parse_final_content(file_binary)

        
        new_emails.append(Email(
            public_id=item.id,
            content=content,
            group_id=group.id,
            user_id=current_user.id,
            
        ))


    session.add_all(new_emails)
    session.commit()

    for email in new_emails:
        session.refresh(email)

    email_payload =  [{"id": e.id, "content": e.content} for e in new_emails]

    background_tasks.add_task(analyze_emails_task, email_payload)


    return {"message": f"Added {len(new_emails)} emails to group {group_id}"}
    