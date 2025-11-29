import uuid
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

# Imports from your project structure
from database.models import User, Session 
from backend.schemas import UserAuth, LoginResponse
from backend.utils.security import verify_password, get_password_hash
from backend.dependencies import get_db

router = APIRouter(
    tags=["Authentication"],
    prefix='/auth'
)

def create_session_for_user(db: Session, user_id: int, response: Response):
    """
    Creates a DB session, sets the cookie, and returns the Passport JSON.
    Used by both Login and Signup.
    """
    # 1. Construct Passport/Express-session style JSON
    session_content = {
        "cookie": {
            "originalMaxAge": None,
            "expires": None,
            "httpOnly": True,
            "path": "/"
        },
        "passport": {
            "user": {
                "id": user_id
            }
        }
    }

    # 2. Create Session in DB
    session_id = str(uuid.uuid4())
    # Calculate expiration (24 hours)
    expiration = datetime.now(timezone.utc) + timedelta(hours=24)

    new_session = Session(
        sid=session_id,
        sess=session_content, 
        expire=expiration
    )
    db.add(new_session)
    db.commit()

    # 3. Set the Cookie on the Response object
    response.set_cookie(
        key="connect.sid",
        value=session_id,
        httponly=True,
        max_age=86400, # 24 hours in seconds
        samesite="lax",
        path="/"
    )

    # 4. Return the JSON content
    return session_content

@router.post("/signup", status_code=201)
def signup(user_data: UserAuth, response: Response, db: Session = Depends(get_db)):
    # 1. Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(status_code=400, detail="Username already registered")

    # 2. Create User
    hashed_pw = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, pass_hash=hashed_pw)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # 3. Auto-Login (Create session + Cookie)
    return create_session_for_user(db, new_user.id, response)

@router.post("/login", response_model=LoginResponse)
def login(user_data: UserAuth, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_data.username).first()
    if not user or not verify_password(user_data.password, user.pass_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    # 2. Login (Create session + Cookie)
    return create_session_for_user(db, user.id, response)

