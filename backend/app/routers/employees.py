"""
Employee API routes.
"""
from fastapi import APIRouter
from typing import List

from app.models.employee import AIEmployee, AIEmployeeCreate
from app.services.employee_service import employee_service

router = APIRouter(prefix="/employees", tags=["employees"])

@router.post("", response_model=AIEmployee)
async def create_employee(employee: AIEmployeeCreate):
    """Create a new AI employee."""
    return employee_service.create_employee(employee)

@router.get("", response_model=List[AIEmployee])
async def get_employees():
    """Get all employees."""
    return employee_service.get_all_employees()

@router.get("/{employee_id}", response_model=AIEmployee)
async def get_employee(employee_id: str):
    """Get a specific employee by ID."""
    return employee_service.get_employee(employee_id)

@router.delete("/{employee_id}")
async def delete_employee(employee_id: str):
    """Delete an employee."""
    return employee_service.delete_employee(employee_id)
