from pydantic import BaseModel

class GroupOut(BaseModel):
    group_id: str
    name: str

class GroupCreate(BaseModel):
    group_id: str
    name: str