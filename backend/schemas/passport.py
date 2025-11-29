from pydantic import BaseModel

class CookieObj(BaseModel):
    originalMaxAge: int | None = None
    expires: str | None = None
    httpOnly: bool = True
    path: str = "/"

class UserIDObj(BaseModel):
    id: int

class PassportObj(BaseModel):
    user: UserIDObj

class LoginResponse(BaseModel):
    cookie: CookieObj
    passport: PassportObj