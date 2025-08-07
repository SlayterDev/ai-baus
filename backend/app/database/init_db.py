"""
Database initialization and sample data.
"""
from sqlalchemy.orm import Session
from app.database.database import engine, Base
from app.database.models import Employee
from datetime import datetime


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def init_sample_data(db: Session):
    """Initialize the database with sample employees."""
    # Check if employees already exist
    existing_employees = db.query(Employee).count()
    if existing_employees > 0:
        return
    
    # Create sample employees
    sample_employees = [
        Employee(
            name="Dinkleberg",
            role="Project Manager",
            personality="Butt kissing, overachiever",
            expertise=["Project Management", "Team Leadership", "Viral Programming Tools"],
            llm_provider="openai",
            llm_model="gpt-4.1-2025-04-14",
            system_prompt=None,
            is_active=True
        ),
        Employee(
            name="McStuffins",
            role="Software Engineer",
            personality="Nihilistic, worked here way too long, and a bit of a know-it-all",
            expertise=["Software Development", "AI Programming", "Problem Solving"],
            llm_provider="openai",
            llm_model="gpt-4.1-2025-04-14",
            system_prompt=None,
            is_active=True
        )
    ]
    
    for employee in sample_employees:
        db.add(employee)
    
    db.commit()
    print("Sample data initialized successfully!")
