"""
SQLAlchemy database models.
"""
from sqlalchemy import Column, String, DateTime, Boolean, Text, JSON, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from app.database.database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    personality = Column(String(500), nullable=False)
    expertise = Column(JSON, nullable=False, default=list)  # Store as JSON array
    llm_provider = Column(String(50), nullable=False)
    llm_model = Column(String(100), nullable=False)
    system_prompt = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    messages = relationship("Message", back_populates="sender")


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    employee_ids = Column(JSON, nullable=False)  # Store as JSON array
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_active = Column(Boolean, default=True)

    # Relationships
    messages = relationship("Message", back_populates="meeting")


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    meeting_id = Column(UUID(as_uuid=True), ForeignKey("meetings.id"), nullable=False)
    content = Column(String(1000), nullable=False)
    sender_type = Column(String(20), nullable=False)  # 'user' or 'employee'
    sender_id = Column(UUID(as_uuid=True), ForeignKey("employees.id"), nullable=True)
    sender_name = Column(String(100), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    meeting = relationship("Meeting", back_populates="messages")
    sender = relationship("Employee", back_populates="messages")
