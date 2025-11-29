from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.orm import Session as db_Session
from datetime import datetime, timezone
from database.db import SessionLocal
from database.models import User, Session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(request: Request, db: db_Session = Depends(get_db)):
    # 1. Get the cookie
    session_id = request.cookies.get("connect.sid")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # 2. Find the session in DB
    db_session = db.query(Session).filter(Session.sid == session_id).first()
    
    if not db_session:
        raise HTTPException(status_code=401, detail="Invalid session")

    # 3. Check expiration
    # Ensure both datetimes are timezone-aware for comparison
    now = datetime.now(timezone.utc)
    if db_session.expire < now:
        raise HTTPException(status_code=401, detail="Session expired")

    # 4. Extract User ID from the JSON payload
    # Structure: {"passport": {"user": {"id": 1}}}
    try:
        user_id = db_session.sess["passport"]["user"]["id"]
    except KeyError:
        raise HTTPException(status_code=401, detail="Malformed session data")

    # 5. Fetch the actual User
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
        
    return user