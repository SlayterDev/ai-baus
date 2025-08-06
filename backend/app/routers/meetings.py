"""
Meeting API routes.
"""
from fastapi import APIRouter
from typing import List

from app.models.meeting import Meeting, MeetingCreate
from app.services.meeting_service import meeting_service

router = APIRouter(prefix="/meetings", tags=["meetings"])

@router.post("", response_model=Meeting)
async def create_meeting(meeting: MeetingCreate):
    """Create a new meeting."""
    return meeting_service.create_meeting(meeting)

@router.get("", response_model=List[Meeting])
async def get_meetings():
    """Get all meetings."""
    return meeting_service.get_all_meetings()

@router.get("/{meeting_id}", response_model=Meeting)
async def get_meeting(meeting_id: str):
    """Get a specific meeting by ID."""
    return meeting_service.get_meeting(meeting_id)
