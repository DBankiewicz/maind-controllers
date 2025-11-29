from fastapi import APIRouter, Depends
from database.models import users as models
from backend.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
def read_my_profile(current_user: models.User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "message": "Welcome back!"
    }