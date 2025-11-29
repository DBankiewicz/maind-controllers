import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response, status, BackgroundTasks, UploadFile
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import update

# Imports from your project structure
from database.models import User, Email, Group, EmailAnalysis
from backend.schemas import EmailIn
from backend.dependencies import get_db, get_current_user

from backend.ai_core.data_loader.load_data import process_mail
from database.db import SessionLocal 
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
                db_analysis = EmailAnalysis(
                    public_id=str(uuid.uuid4()),
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

            except:
                session.rollback()
                continue
        

async def parse_final_content(file_content: UploadFile) -> str:
    content_bytes = await file_content.read()
    try:
        return content_bytes.decode('utf-8')
    except Exception:
        return "[Error]: Binary file could not be parsed"

@router.post('/', status_code=status.HTTP_202_ACCEPTED)
async def add_and_analyze(group_id: str, 
                    emails: List[EmailIn], 
                    background_tasks: BackgroundTasks,
                    current_user: User = Depends(get_current_user),
                    session: Session = Depends(get_db)):
    group = session.query(Group).where(Group.public_id==group_id).first()
    if not group:
        raise HTTPException(404, detail="No group with such id")
    
    if group.user_id != current_user.id:
        raise HTTPException(401, detail="You are not authorized to add emails to this group.")
    
    new_emails = []
    for item in emails:
        content = item.content
        if content is None:
            content = await parse_final_content(item[item.file_key])
        
        new_emails.append(Email(
            public_id=item.id,
            content=content,
            user_id=current_user.id,
            group_id=group.id
        ))


    session.add_all(new_emails)
    session.commit()

    for email in new_emails:
        session.refresh(email)

    email_payload =  [{"id": e.id, "content": e.content} for e in new_emails]

    background_tasks.add_task(analyze_emails_task, email_payload)


    return {"message": f"Added {len(new_emails)} emails to group {group_id}"}
    