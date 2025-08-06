"""
Message API routes.
"""
from fastapi import APIRouter
from typing import List

from app.models.message import Message, MessageCreate
from app.services.message_service import message_service

router = APIRouter(prefix="/meetings", tags=["messages"])

@router.post("/{meeting_id}/messages", response_model=Message)
async def send_message(meeting_id: str, message: MessageCreate):
    """Send a message to a meeting."""
    return message_service.send_message(meeting_id, message)

@router.post("/{meeting_id}/messages/{employee_id}/respond", response_model=Message)
async def respond_to_message(meeting_id: str, employee_id: str):
    """Generate an AI employee response to the conversation."""
    return await message_service.generate_employee_response(meeting_id, employee_id)

@router.get("/{meeting_id}/messages", response_model=List[Message])
async def get_messages(meeting_id: str):
    """Get all messages for a meeting."""
    return message_service.get_messages(meeting_id)
