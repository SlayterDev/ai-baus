"""
Message-related Pydantic models.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MessageCreate(BaseModel):
    meeting_id: str
    content: str = Field(..., min_length=1, max_length=1000)
    sender_type: str = Field(..., pattern="^(user|employee)$")
    sender_id: Optional[str] = None  # employee ID if sender_type is 'employee'

class Message(BaseModel):
    id: str
    meeting_id: str
    content: str
    sender_type: str
    sender_id: Optional[str]
    sender_name: str
    timestamp: datetime
