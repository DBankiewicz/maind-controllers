from fastapi import FastAPI
from backend.routers import auth, user, email, group

# Initialize App
app = FastAPI(title="My Project API")

# Include Routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(email.router)
app.include_router(group.router)


@app.get("/")
def health_check():
    return {"status": "ok", "message": "Go to /docs to test login"}