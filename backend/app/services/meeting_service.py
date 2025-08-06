"""
Meeting service for business logic related to meetings.
"""
import uuid
from datetime import datetime
from typing import List
from fastapi import HTTPException

from app.models.meeting import Meeting, MeetingCreate
from app.database.memory_store import meetings_db, messages_db, employees_db

class MeetingService:
    
    @staticmethod
    def create_meeting(meeting_data: MeetingCreate) -> Meeting:
        """Create a new meeting."""
        # Validate that all employees exist
        for emp_id in meeting_data.employee_ids:
            if emp_id not in employees_db:
                raise HTTPException(status_code=400, detail=f"Employee {emp_id} not found")
        
        meeting_id = str(uuid.uuid4())
        new_meeting = Meeting(
            id=meeting_id,
            title=meeting_data.title,
            description=meeting_data.description,
            employee_ids=meeting_data.employee_ids,
            created_at=datetime.now(),
            is_active=True
        )
        
        meetings_db[meeting_id] = new_meeting
        messages_db[meeting_id] = []  # Initialize message history for the meeting
        
        return new_meeting
    
    @staticmethod
    def get_all_meetings() -> List[Meeting]:
        """Get all meetings."""
        return list(meetings_db.values())
    
    @staticmethod
    def get_meeting(meeting_id: str) -> Meeting:
        """Get a specific meeting by ID."""
        if meeting_id not in meetings_db:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return meetings_db[meeting_id]

# Global instance
meeting_service = MeetingService()
