"""
Employee-related Pydantic models.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class AIEmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=100)
    personality: str = Field(..., min_length=1, max_length=500)
    expertise: List[str] = Field(default_factory=list)
    llm_provider: str = Field(..., pattern="^(openai|anthropic)$")
    llm_model: str
    system_prompt: Optional[str] = None

class AIEmployee(BaseModel):
    id: str
    name: str
    role: str
    personality: str
    expertise: List[str]
    llm_provider: str
    llm_model: str
    system_prompt: Optional[str] = None
    created_at: datetime
    is_active: bool = True
