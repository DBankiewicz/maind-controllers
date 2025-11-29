from fastapi import FastAPI
from backend.routers import auth, users

# Initialize App
app = FastAPI(title="My Project API")

# Include Routers
app.include_router(auth.router)
app.include_router(users.router)

# Example of how you would add more routers later:
# from routers import users
# app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
def health_check():
    return {"status": "ok", "message": "Go to /docs to test login"}