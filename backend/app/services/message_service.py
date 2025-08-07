"""
Message service for business logic related to messages.
"""
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.message import Message, MessageCreate
from app.database.repositories import MessageRepository, MeetingRepository, EmployeeRepository
from app.services.llm_service import llm_service

class MessageService:
    
    @staticmethod
    def send_message(meeting_id: str, message_data: MessageCreate, db: Session) -> Message:
        """Send a message to a meeting."""
        # Validate meeting exists
        meeting_repo = MeetingRepository(db)
        if not meeting_repo.get_by_id(meeting_id):
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        if message_data.sender_type == "user":
            sender_name = "User"
        else:
            employee_repo = EmployeeRepository(db)
            employee = employee_repo.get_by_id(message_data.sender_id)
            if not employee:
                raise HTTPException(status_code=400, detail="Employee not found")
            sender_name = employee.name
        
        message_repo = MessageRepository(db)
        return message_repo.create(message_data, sender_name)
    
    @staticmethod
    async def generate_employee_response(meeting_id: str, employee_id: str, db: Session) -> Message:
        """Generate an AI employee response to the conversation."""
        # Validate meeting and employee exist
        meeting_repo = MeetingRepository(db)
        employee_repo = EmployeeRepository(db)
        message_repo = MessageRepository(db)
        
        meeting = meeting_repo.get_by_id(meeting_id)
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")

        # employee = employee_repo.get_by_id(employee_id)
        # if not employee:
        #     raise HTTPException(status_code=404, detail="Employee not found")
        # get list of employees in the meeting
        employees = employee_repo.get_by_meeting_id(meeting_id)
        if not employees:
            raise HTTPException(status_code=404, detail="No employees found for this meeting")

        conversation_history = message_repo.get_by_meeting_id(meeting_id)[-1]

        if not conversation_history:
            raise HTTPException(status_code=400, detail="No conversation history found for this meeting")

        response_content = await llm_service.generate_crew_response(meeting=meeting, employees=employees, new_message=conversation_history)

        # Create the response message
        message_data = MessageCreate(
            meeting_id=meeting_id,
            content=response_content,
            sender_type="employee",
            sender_id=employee_id
        )

        return message_repo.create(message_data, "Crew Response")
    
    @staticmethod
    def get_messages(meeting_id: str, db: Session) -> List[Message]:
        """Get all messages for a meeting."""
        meeting_repo = MeetingRepository(db)
        if not meeting_repo.get_by_id(meeting_id):
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        message_repo = MessageRepository(db)
        return message_repo.get_by_meeting_id(meeting_id)

# Global instance
message_service = MessageService()
