"""
Employee service for business logic related to AI employees.
"""
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.employee import AIEmployee, AIEmployeeCreate
from app.database.repositories import EmployeeRepository
from app.services.llm_service import llm_service

class EmployeeService:
    
    @staticmethod
    def create_employee(employee_data: AIEmployeeCreate, db: Session) -> AIEmployee:
        """Create a new AI employee."""
        employee_repo = EmployeeRepository(db)
        
        # Create the employee first to get an ID
        new_employee = employee_repo.create(employee_data)
        
        # Generate system prompt using LLM service if not provided
        if not employee_data.system_prompt:
            system_prompt = llm_service._create_system_prompt(new_employee)
            # Update the employee with the generated system prompt
            updated_data = AIEmployeeCreate(
                name=employee_data.name,
                role=employee_data.role,
                personality=employee_data.personality,
                expertise=employee_data.expertise,
                llm_provider=employee_data.llm_provider,
                llm_model=employee_data.llm_model,
                system_prompt=system_prompt
            )
            new_employee = employee_repo.update(new_employee.id, updated_data)
        
        return new_employee
    
    @staticmethod
    def get_all_employees(db: Session) -> List[AIEmployee]:
        """Get all employees."""
        employee_repo = EmployeeRepository(db)
        return employee_repo.get_all()
    
    @staticmethod
    def get_employee(employee_id: str, db: Session) -> AIEmployee:
        """Get a specific employee by ID."""
        employee_repo = EmployeeRepository(db)
        employee = employee_repo.get_by_id(employee_id)
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employee
    
    @staticmethod
    def delete_employee(employee_id: str, db: Session) -> dict:
        """Delete an employee."""
        employee_repo = EmployeeRepository(db)
        if not employee_repo.delete(employee_id):
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {"message": "Employee deleted successfully"}

# Global instance
employee_service = EmployeeService()
