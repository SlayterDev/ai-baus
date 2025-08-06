from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json
import uuid
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Boss Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

class MeetingCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    employee_ids: List[str] = Field(..., min_items=2)

class Meeting(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    employee_ids: List[str]
    created_at: datetime
    is_active: bool = True

class MessageCreate(BaseModel):
    meeting_id: str
    content: str = Field(..., min_length=1, max_length=1000)
    sender_type: str = Field(..., pattern="^(user|employee)$")
    sender_id: Optional[str] = None # employee ID if sender_type is 'employee'

class Message(BaseModel):
    id: str
    meeting_id: str
    content: str
    sender_type: str
    sender_id: Optional[str]
    sender_name: str
    timestamp: datetime

# in-memory database simulation
employees_db = {
    '9c44c489-7b30-433d-be0c-d94d0676c15a': AIEmployee(
        id="9c44c489-7b30-433d-be0c-d94d0676c15a",
        name="Dinkleberg",
        role="Project Manager",
        personality="Butt kissing, overachiever",
        expertise=["Project Management", "Team Leadership", "Viral Programming Tools"],
        llm_provider="openai",
        llm_model="gpt-4.1-2025-04-14",
        system_prompt=None,
        created_at=datetime.now(),
        is_active=True
    ),
    '8c11cb9a-8dfd-4903-b553-634a993a0c3a': AIEmployee(
        id="8c11cb9a-8dfd-4903-b553-634a993a0c3a",
        name="McStuffins",
        role="Software Engineer",
        personality="Nihilistic, worked here way too long, and a bit of a know-it-all",
        expertise=["Software Development", "AI Programming", "Problem Solving"],
        llm_provider="openai",
        llm_model="gpt-4.1-2025-04-14",
        system_prompt=None,
        created_at=datetime.now(),
        is_active=True
    )
}
meetings_db = {}
messages_db = {}

class LLMManager:
    def __init__(self):
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    async def generate_response(self, employee: AIEmployee, conversation_history: List[Message]) -> str:
        """Generate a response using the specified LLM provider based on the conversation history and new message."""
        try:
            if employee.llm_provider == "openai":
                return await self._generate_openai_response(employee, conversation_history)
            elif employee.llm_provider == "anthropic":
                return await self._generate_anthropic_response(employee, conversation_history)
            else:
                raise ValueError("Unsupported LLM provider")
        except Exception as e:
            return f"Error generating response: {str(e)}"

    async def _generate_openai_response(self, employee: AIEmployee, conversation_history: List[Message]) -> str:
        if not self.openai_key:
            raise ValueError("OpenAI API key is not set")
        
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.openai_key)
        except ImportError:
            raise ValueError("OpenAI library not installed. Please install with: pip install openai")

        messages = [{"role": "system", "content": employee.system_prompt or create_system_prompt(employee)}]

        for msg in conversation_history[-10:]:
            role = "assistant" if msg.sender_type == "employee" else "user"
            messages.append({"role": role, "content": f"{msg.sender_name}: {msg.content}"})

        try:
            response = await client.chat.completions.create(
                model=employee.llm_model,
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise ValueError(f"OpenAI API error: {str(e)}")

    async def _generate_anthropic_response(self, employee: AIEmployee, conversation_history: List[Message]) -> str:
        if not self.anthropic_key:
            raise ValueError("Anthropic API key is not set")
        
        import anthropic
        client = anthropic.AsyncAnthropic(api_key=self.anthropic_key)

        conversation = ""
        for msg in conversation_history[-10:]:
            conversation += f"{msg.sender_name}: {msg.content}\n"

        prompt = f"{employee.system_prompt or create_system_prompt(employee)}\n\nConversation:\n{conversation}\n{employee.name}:"

        response = await client.completions.create(
            model=employee.llm_model,
            prompt=prompt,
            max_tokens_to_sample=300,
            temperature=0.7
        )

        return response.completion.strip()

llm_manager = LLMManager()

def create_system_prompt(employee: AIEmployee) -> str:
    """Create a system prompt based on the employee's personality and expertise."""
    expertise_str = ", ".join(employee.expertise) if employee.expertise else "general knowledge"
    prompt = f"""You are {employee.name}, a {employee.role} AI Employee.

Personality: {employee.personality}

Your area of expertise includes: {expertise_str}.

Instructions:
- Stay in character as {employee.name}.
- Be helpful, professional, and embody your personality.
- Keep responses concise and relevant to the conversation. (1-3 sentences unless more detail is requested)
- In meetings, collaborate effectively with other AI employees.
- If asked about something outside your expertise, acknowledge it and suggest consulting another employee or resource.
- If you don't know the answer, it's okay to say so.
- Don't label your messages with your name or role; just respond naturally.
"""
    
    return employee.system_prompt or prompt

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Boss Backend!", "version": "0.1.0"}

# Employee Endpoints
@app.post("/employees", response_model=AIEmployee)
async def create_employee(employee: AIEmployeeCreate):
    employee_id = str(uuid.uuid4())
    new_employee = AIEmployee(
        id=employee_id,
        name=employee.name,
        role=employee.role,
        personality=employee.personality,
        expertise=employee.expertise,
        llm_provider=employee.llm_provider,
        llm_model=employee.llm_model,
        system_prompt=create_system_prompt(employee),
        created_at=datetime.now(),
        is_active=True
    )
    employees_db[employee_id] = new_employee
    return new_employee

@app.get("/employees", response_model=List[AIEmployee])
async def get_employees():
    return list(employees_db.values())

@app.get("/employees/{employee_id}", response_model=AIEmployee)
async def get_employee(employee_id: str):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employees_db[employee_id]

@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    for meeting in meetings_db.values():
        if employee_id in meeting.employee_ids:
            meeting.employee_ids.remove(employee_id)
    
    del employees_db[employee_id]
    return {"message": "Employee deleted successfully"}

# Meeting Endpoints
@app.post("/meetings", response_model=Meeting)
async def create_meeting(meeting: MeetingCreate):
    for emp_id in meeting.employee_ids:
        if emp_id not in employees_db:
            raise HTTPException(status_code=400, detail=f"Employee {emp_id} not found")
    
    meeting_id = str(uuid.uuid4())
    new_meeting = Meeting(
        id=meeting_id,
        title=meeting.title,
        description=meeting.description,
        employee_ids=meeting.employee_ids,
        created_at=datetime.now(),
        is_active=True
    )
    
    meetings_db[meeting_id] = new_meeting
    messages_db[meeting_id] = []  # Initialize message history for the meeting
    
    return new_meeting

@app.get("/meetings", response_model=List[Meeting])
async def get_meetings():
    return list(meetings_db.values())

@app.get("/meetings/{meeting_id}", response_model=Meeting)
async def get_meeting(meeting_id: str):
    if meeting_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")
    return meetings_db[meeting_id]

# Message Endpoints
@app.post("/meetings/{meeting_id}/messages", response_model=Message)
async def send_message(meeting_id: str, message: MessageCreate):
    if meeting_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    meeting = meetings_db[meeting_id]

    if message.sender_type == "user":
        sender_name = "User"
    else:
        if message.sender_id not in employees_db:
            raise HTTPException(status_code=400, detail="Employee not found")
        sender_name = employees_db[message.sender_id].name
    
    new_message = Message(
        id=str(uuid.uuid4()),
        meeting_id=meeting_id,
        content=message.content,
        sender_type=message.sender_type,
        sender_id=message.sender_id,
        sender_name=sender_name,
        timestamp=datetime.now()
    )
    
    messages_db[meeting_id].append(new_message)
    
    return new_message

@app.post("/meetings/{meeting_id}/messages/{employee_id}/respond", response_model=Message)
async def respond_to_message(meeting_id: str, employee_id: str):
    if meeting_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")

    if employee_id not in employees_db:
        raise HTTPException(status_code=404, detail="Employee not found")

    employee = employees_db[employee_id]

    conversation_history = messages_db.get(meeting_id, [])

    if not conversation_history:
        raise HTTPException(status_code=400, detail="No conversation history found for this meeting")

    response_content = await llm_manager.generate_response(employee, conversation_history)

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

@app.get("/meetings/{meeting_id}/messages", response_model=List[Message])
async def get_messages(meeting_id: str):
    if meeting_id not in meetings_db:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return messages_db.get(meeting_id, [])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
