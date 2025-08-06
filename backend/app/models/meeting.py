"""
Meeting-related Pydantic models.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class MeetingCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    employee_ids: List[str] = Field(..., min_items=2)

class Meeting(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    employee_ids: List[str]
    created_at: datetime
    is_active: bool = True
