"""
Meeting service for business logic related to meetings.
"""
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.meeting import Meeting, MeetingCreate
from app.database.repositories import MeetingRepository, EmployeeRepository

class MeetingService:
    
    @staticmethod
    def create_meeting(meeting_data: MeetingCreate, db: Session) -> Meeting:
        """Create a new meeting."""
        # Validate that all employees exist
        employee_repo = EmployeeRepository(db)
        for emp_id in meeting_data.employee_ids:
            if not employee_repo.get_by_id(emp_id):
                raise HTTPException(status_code=400, detail=f"Employee {emp_id} not found")
        
        meeting_repo = MeetingRepository(db)
        return meeting_repo.create(meeting_data)
    
    @staticmethod
    def get_all_meetings(db: Session) -> List[Meeting]:
        """Get all meetings."""
        meeting_repo = MeetingRepository(db)
        return meeting_repo.get_all()
    
    @staticmethod
    def get_meeting(meeting_id: str, db: Session) -> Meeting:
        """Get a specific meeting by ID."""
        meeting_repo = MeetingRepository(db)
        meeting = meeting_repo.get_by_id(meeting_id)
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return meeting

# Global instance
meeting_service = MeetingService()
