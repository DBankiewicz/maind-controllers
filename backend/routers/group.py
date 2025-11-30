import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session, joinedload
from typing import List

# Imports from your project structure
from database.models import User, Email, Group
from backend.schemas import EmailAnalysisSchema, GroupOut, GroupCreate, EmailWithAnalysis, EmailOut
from backend.dependencies import get_db, get_current_user


router = APIRouter(
    tags=["Authentication"],
    prefix='/group'
)

@router.post('', response_model=GroupOut)
def create_group(group_data: GroupCreate,
                 current_user:User = Depends(get_current_user), 
                 session: Session = Depends(get_db)):
    new_group = Group(
        public_id=group_data.group_id,
        name=group_data.name,
        user_id=current_user.id
    )

    session.add(new_group)
    session.commit()
    session.refresh(new_group)

    return {
        "group_id": new_group.public_id,
        "name": new_group.name
    }

@router.get('', response_model=List[GroupOut])
def get_groups(current_user:User = Depends(get_current_user), 
                 session: Session = Depends(get_db)):
    result = []

    groups = session.query(Group).where(Group.user_id==current_user.id).all()

    for item in groups:
        result.append({
            "group_id": item.public_id,
            "name": item.name
        })

    return result

@router.options('')
def dummy():
    return {"d": "ummy"}


@router.get('/status/{group_id}')
def get_group_status(group_id: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    group = session.query(Group).where(Group.public_id==group_id).first()
    if (group.user_id != current_user.id):
        raise HTTPException(400, "Unauthorized")


    return {"status": group.status}

@router.get('/{group_id}', response_class=List[EmailWithAnalysis])
def get_group_emails(group_id: str, current_user: User = Depends(get_current_user), session: Session = Depends(get_db)):
    group = session.query(Group).where(Group.public_id==group_id).first()
    if (group.user_id != current_user.id):
        raise HTTPException(400, "Unauthorized")
    
    emails = session.query(Email).options(joinedload(Email.analysis)).where(Email.group_id == group_id).all()

    res = []
    for email in emails:
        analysis = email.analysis
        res.append(EmailWithAnalysis(
            email_raw=EmailOut(
                id=email.public_id,
                text=email.content
            ),
            analysis=EmailAnalysisSchema(
                sender=analysis.sender,
                recepients=analysis.recepients,
                topic=analysis.topic,
                summary=analysis.summary,
                timestamp=analysis.timestamp,
                extra=analysis.extra
            )
        ))

    return res