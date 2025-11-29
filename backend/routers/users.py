from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.models import users as models
from backend.schemas import UserOut, UserUpdate
from backend.dependencies import get_db, get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/users/me")
def read_my_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "message": "Welcome back!"
    }