"""
Database repository classes for data access.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
import uuid

from app.database.models import Employee as DBEmployee, Meeting as DBMeeting, Message as DBMessage
from app.models.employee import AIEmployee, AIEmployeeCreate
from app.models.meeting import Meeting, MeetingCreate
from app.models.message import Message, MessageCreate


class EmployeeRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, employee_data: AIEmployeeCreate) -> AIEmployee:
        """Create a new employee."""
        db_employee = DBEmployee(
            name=employee_data.name,
            role=employee_data.role,
            personality=employee_data.personality,
            expertise=employee_data.expertise,
            llm_provider=employee_data.llm_provider,
            llm_model=employee_data.llm_model,
            system_prompt=employee_data.system_prompt
        )
        self.db.add(db_employee)
        self.db.commit()
        self.db.refresh(db_employee)
        return self._to_pydantic(db_employee)

    def get_by_id(self, employee_id: str) -> Optional[AIEmployee]:
        """Get an employee by ID."""
        db_employee = self.db.query(DBEmployee).filter(
            and_(DBEmployee.id == employee_id, DBEmployee.is_active == True)
        ).first()
        return self._to_pydantic(db_employee) if db_employee else None

    def get_all(self) -> List[AIEmployee]:
        """Get all active employees."""
        db_employees = self.db.query(DBEmployee).filter(DBEmployee.is_active == True).all()
        return [self._to_pydantic(emp) for emp in db_employees]

    def update(self, employee_id: str, employee_data: AIEmployeeCreate) -> Optional[AIEmployee]:
        """Update an employee."""
        db_employee = self.db.query(DBEmployee).filter(
            and_(DBEmployee.id == employee_id, DBEmployee.is_active == True)
        ).first()
        
        if not db_employee:
            return None
        
        for field, value in employee_data.dict().items():
            setattr(db_employee, field, value)
        
        self.db.commit()
        self.db.refresh(db_employee)
        return self._to_pydantic(db_employee)

    def delete(self, employee_id: str) -> bool:
        """Soft delete an employee."""
        db_employee = self.db.query(DBEmployee).filter(
            and_(DBEmployee.id == employee_id, DBEmployee.is_active == True)
        ).first()
        
        if not db_employee:
            return False
        
        db_employee.is_active = False
        self.db.commit()
        return True

    def _to_pydantic(self, db_employee: DBEmployee) -> AIEmployee:
        """Convert database model to Pydantic model."""
        return AIEmployee(
            id=str(db_employee.id),
            name=db_employee.name,
            role=db_employee.role,
            personality=db_employee.personality,
            expertise=db_employee.expertise,
            llm_provider=db_employee.llm_provider,
            llm_model=db_employee.llm_model,
            system_prompt=db_employee.system_prompt,
            created_at=db_employee.created_at,
            is_active=db_employee.is_active
        )


class MeetingRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, meeting_data: MeetingCreate) -> Meeting:
        """Create a new meeting."""
        db_meeting = DBMeeting(
            title=meeting_data.title,
            description=meeting_data.description,
            employee_ids=meeting_data.employee_ids
        )
        self.db.add(db_meeting)
        self.db.commit()
        self.db.refresh(db_meeting)
        return self._to_pydantic(db_meeting)

    def get_by_id(self, meeting_id: str) -> Optional[Meeting]:
        """Get a meeting by ID."""
        db_meeting = self.db.query(DBMeeting).filter(
            and_(DBMeeting.id == meeting_id, DBMeeting.is_active == True)
        ).first()
        return self._to_pydantic(db_meeting) if db_meeting else None

    def get_all(self) -> List[Meeting]:
        """Get all active meetings."""
        db_meetings = self.db.query(DBMeeting).filter(DBMeeting.is_active == True).all()
        return [self._to_pydantic(meeting) for meeting in db_meetings]

    def delete(self, meeting_id: str) -> bool:
        """Soft delete a meeting."""
        db_meeting = self.db.query(DBMeeting).filter(
            and_(DBMeeting.id == meeting_id, DBMeeting.is_active == True)
        ).first()
        
        if not db_meeting:
            return False
        
        db_meeting.is_active = False
        self.db.commit()
        return True

    def _to_pydantic(self, db_meeting: DBMeeting) -> Meeting:
        """Convert database model to Pydantic model."""
        return Meeting(
            id=str(db_meeting.id),
            title=db_meeting.title,
            description=db_meeting.description,
            employee_ids=db_meeting.employee_ids,
            created_at=db_meeting.created_at,
            is_active=db_meeting.is_active
        )


class MessageRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, message_data: MessageCreate, sender_name: str) -> Message:
        """Create a new message."""
        db_message = DBMessage(
            meeting_id=message_data.meeting_id,
            content=message_data.content,
            sender_type=message_data.sender_type,
            sender_id=message_data.sender_id,
            sender_name=sender_name
        )
        self.db.add(db_message)
        self.db.commit()
        self.db.refresh(db_message)
        return self._to_pydantic(db_message)

    def get_by_meeting_id(self, meeting_id: str) -> List[Message]:
        """Get all messages for a meeting."""
        db_messages = self.db.query(DBMessage).filter(
            DBMessage.meeting_id == meeting_id
        ).order_by(DBMessage.timestamp).all()
        return [self._to_pydantic(msg) for msg in db_messages]

    def _to_pydantic(self, db_message: DBMessage) -> Message:
        """Convert database model to Pydantic model."""
        return Message(
            id=str(db_message.id),
            meeting_id=str(db_message.meeting_id),
            content=db_message.content,
            sender_type=db_message.sender_type,
            sender_id=str(db_message.sender_id) if db_message.sender_id else None,
            sender_name=db_message.sender_name,
            timestamp=db_message.timestamp
        )
