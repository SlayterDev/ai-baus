"""
Employee service for business logic related to AI employees.
"""
import uuid
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException

from app.models.employee import AIEmployee, AIEmployeeCreate
from app.database.memory_store import employees_db, meetings_db
from app.services.llm_service import llm_service

class EmployeeService:
    
    @staticmethod
    def create_employee(employee_data: AIEmployeeCreate) -> AIEmployee:
        """Create a new AI employee."""
        employee_id = str(uuid.uuid4())
        
        # Create system prompt using LLM service
        system_prompt = llm_service._create_system_prompt(AIEmployee(
            id=employee_id,
            name=employee_data.name,
            role=employee_data.role,
            personality=employee_data.personality,
            expertise=employee_data.expertise,
            llm_provider=employee_data.llm_provider,
            llm_model=employee_data.llm_model,
            system_prompt=employee_data.system_prompt,
            created_at=datetime.now(),
            is_active=True
        ))
        
        new_employee = AIEmployee(
            id=employee_id,
            name=employee_data.name,
            role=employee_data.role,
            personality=employee_data.personality,
            expertise=employee_data.expertise,
            llm_provider=employee_data.llm_provider,
            llm_model=employee_data.llm_model,
            system_prompt=employee_data.system_prompt or system_prompt,
            created_at=datetime.now(),
            is_active=True
        )
        
        employees_db[employee_id] = new_employee
        return new_employee
    
    @staticmethod
    def get_all_employees() -> List[AIEmployee]:
        """Get all employees."""
        return list(employees_db.values())
    
    @staticmethod
    def get_employee(employee_id: str) -> AIEmployee:
        """Get a specific employee by ID."""
        if employee_id not in employees_db:
            raise HTTPException(status_code=404, detail="Employee not found")
        return employees_db[employee_id]
    
    @staticmethod
    def delete_employee(employee_id: str) -> dict:
        """Delete an employee and remove them from meetings."""
        if employee_id not in employees_db:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        # Remove employee from all meetings
        for meeting in meetings_db.values():
            if employee_id in meeting.employee_ids:
                meeting.employee_ids.remove(employee_id)
        
        del employees_db[employee_id]
        return {"message": "Employee deleted successfully"}

# Global instance
employee_service = EmployeeService()
