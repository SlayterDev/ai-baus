"""
LLM service for handling AI model interactions.
"""
from typing import List
from app.models.employee import AIEmployee
from app.models.message import Message
from app.models.meeting import Meeting
from app.config import settings
from app.services.crew_service import crew_service

class LLMService:
    def __init__(self):
        self.openai_key = settings.OPENAI_API_KEY
        self.anthropic_key = settings.ANTHROPIC_API_KEY
    
    async def generate_crew_response(self, meeting: Meeting, employees: List[AIEmployee], new_message: Message) -> str:
        """Generate a response from the crew based on the new message."""
        if not employees or not new_message:
            raise ValueError("Employees and new message must be provided to generate a response")
        
        # Create a crew with the given employees
        crew = crew_service.create_crew(employees)
        
        # Create a task for the crew based on the new message
        task = crew_service.create_task(meeting, new_message)
        
        # Kick off the crew with the task
        crew_output = crew_service.kickoff_crew(crew, task)
        
        return crew_output

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

        messages = [{"role": "system", "content": employee.system_prompt or self._create_system_prompt(employee)}]

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

        prompt = f"{employee.system_prompt or self._create_system_prompt(employee)}\n\nConversation:\n{conversation}\n{employee.name}:"

        response = await client.completions.create(
            model=employee.llm_model,
            prompt=prompt,
            max_tokens_to_sample=300,
            temperature=0.7
        )

        return response.completion.strip()

    def _create_system_prompt(self, employee: AIEmployee) -> str:
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

# Global instance
llm_service = LLMService()
