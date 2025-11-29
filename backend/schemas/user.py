from pydantic import BaseModel, EmailStr

class UserOut(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    email: EmailStr | None = None