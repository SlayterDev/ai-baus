"""
Message service for business logic related to messages.
"""
import uuid
from datetime import datetime
from typing import List
from fastapi import HTTPException

from app.models.message import Message, MessageCreate
from app.database.memory_store import messages_db, meetings_db, employees_db
from app.services.llm_service import llm_service

class MessageService:
    
    @staticmethod
    def send_message(meeting_id: str, message_data: MessageCreate) -> Message:
        """Send a message to a meeting."""
        if meeting_id not in meetings_db:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        if message_data.sender_type == "user":
            sender_name = "User"
        else:
            if message_data.sender_id not in employees_db:
                raise HTTPException(status_code=400, detail="Employee not found")
            sender_name = employees_db[message_data.sender_id].name
        
        new_message = Message(
            id=str(uuid.uuid4()),
            meeting_id=meeting_id,
            content=message_data.content,
            sender_type=message_data.sender_type,
            sender_id=message_data.sender_id,
            sender_name=sender_name,
            timestamp=datetime.now()
        )
        
        messages_db[meeting_id].append(new_message)
        return new_message
    
    @staticmethod
    async def generate_employee_response(meeting_id: str, employee_id: str) -> Message:
        """Generate an AI employee response to the conversation."""
        if meeting_id not in meetings_db:
            raise HTTPException(status_code=404, detail="Meeting not found")

        if employee_id not in employees_db:
            raise HTTPException(status_code=404, detail="Employee not found")

        employee = employees_db[employee_id]
        conversation_history = messages_db.get(meeting_id, [])

        if not conversation_history:
            raise HTTPException(status_code=400, detail="No conversation history found for this meeting")

        response_content = await llm_service.generate_response(employee, conversation_history)

        response_message = Message(
            id=str(uuid.uuid4()),
            meeting_id=meeting_id,
            content=response_content,
            sender_type="employee",
            sender_id=employee.id,
            sender_name=employee.name,
            timestamp=datetime.now()
        )

        messages_db[meeting_id].append(response_message)
        return response_message
    
    @staticmethod
    def get_messages(meeting_id: str) -> List[Message]:
        """Get all messages for a meeting."""
        if meeting_id not in meetings_db:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        return messages_db.get(meeting_id, [])

# Global instance
message_service = MessageService()
