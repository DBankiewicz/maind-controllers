import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

# Imports from your project structure
from database.models import User, Email, Group
from backend.schemas import EmailIn, GroupOut, GroupCreate
from backend.dependencies import get_db, get_current_user


router = APIRouter(
    tags=["Authentication"],
    prefix='/group'
)

@router.post('/', response_model=GroupOut)
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

@router.get('/', response_model=List[GroupOut])
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