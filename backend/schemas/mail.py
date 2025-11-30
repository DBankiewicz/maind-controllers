from pydantic import BaseModel, Field
from typing import Any, List, Optional


class EmailIn(BaseModel):
    id: str
    content: Optional[str]
    file_key: Optional[str]



class EmailAnalysisSchema(BaseModel):
    sender: str = Field(..., description="Sender email address")
    recipients: List[str] = Field(..., description="Recipient email addresses")
    topic: str = Field(..., description="Email topic")
    summary: Optional[str] = Field(None, description="Auto-generated summary of the content")
    extra: dict[str, Any]

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "from_": "alice@example.com",
                "recipients": ["bob@example.com"],
                "topic": "Meeting Update",
                "data": "Hi Bob,\nThe meeting is moved to Monday at 2 PM.\nRegards,\nAlice",
                "summary": "Meeting rescheduled to Monday at 2 PM."
            }
        }

    class Config:
        from_attributes = True

