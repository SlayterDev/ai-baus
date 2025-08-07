"""
Meeting API routes.
"""
from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.models.meeting import Meeting, MeetingCreate
from app.services.meeting_service import meeting_service
from app.database.database import get_db

router = APIRouter(prefix="/meetings", tags=["meetings"])

@router.post("", response_model=Meeting)
async def create_meeting(meeting: MeetingCreate, db: Session = Depends(get_db)):
    """Create a new meeting."""
    return meeting_service.create_meeting(meeting, db)

@router.get("", response_model=List[Meeting])
async def get_meetings(db: Session = Depends(get_db)):
    """Get all meetings."""
    return meeting_service.get_all_meetings(db)

@router.get("/{meeting_id}", response_model=Meeting)
async def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    """Get a specific meeting by ID."""
    return meeting_service.get_meeting(meeting_id, db)
