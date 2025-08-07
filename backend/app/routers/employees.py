"""
Employee API routes.
"""
from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session

from app.models.employee import AIEmployee, AIEmployeeCreate
from app.services.employee_service import employee_service
from app.database.database import get_db

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("", response_model=AIEmployee)
async def create_employee(employee: AIEmployeeCreate, db: Session = Depends(get_db)):
    """Create a new AI employee."""
    return employee_service.create_employee(employee, db)

@router.get("", response_model=List[AIEmployee])
async def get_employees(db: Session = Depends(get_db)):
    """Get all employees."""
    return employee_service.get_all_employees(db)

@router.get("/{employee_id}", response_model=AIEmployee)
async def get_employee(employee_id: str, db: Session = Depends(get_db)):
    """Get a specific employee by ID."""
    return employee_service.get_employee(employee_id, db)

@router.delete("/{employee_id}")
async def delete_employee(employee_id: str, db: Session = Depends(get_db)):
    """Delete an employee."""
    return employee_service.delete_employee(employee_id, db)
