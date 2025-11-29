from pydantic import BaseModel, EmailStr, Field
from typing import Any, List, Optional


class Email(BaseModel):
    from_: EmailStr = Field(..., description="Sender email address")
    to: List[EmailStr] = Field(..., description="Recipient email addresses")
    topic: str = Field(..., description="Email topic or subject")
    data: str = Field(..., description="Full raw email content or body")
    summary: Optional[str] = Field(None, description="Auto-generated summary of the content")
    extra: dict[str, Any ]

    class Config:
        json_schema_extra = {
            "example": {
                "from_": "alice@example.com",
                "to": ["bob@example.com"],
                "topic": "Meeting Update",
                "data": "Hi Bob,\nThe meeting is moved to Monday at 2 PM.\nRegards,\nAlice",
                "summary": "Meeting rescheduled to Monday at 2 PM."
            }
        }
