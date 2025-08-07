"""
Crew service for managing employee interactions and meetings.
"""

from app.models.employee import AIEmployee
from app.models.message import Message
from app.models.meeting import Meeting
from app.config import settings
from crewai import Agent, Crew, Task, Process

class CrewService:
    def __init__(self):
        pass

    def _create_backstory(self, employee: AIEmployee) -> str:
        """Create a backstory for the employee based on their attributes."""
        return f"""
personality: {employee.personality}
expertise: {", ".join(employee.expertise) if employee.expertise else "general knowledge"}
"""

    def create_agent(self, employee: AIEmployee) -> Agent:
        """Create a CrewAI agent for the given employee."""
        if not employee.llm_provider or not employee.llm_model:
            raise ValueError("Employee must have a valid LLM provider and model")

        agent = Agent(
            role=employee.role,
            goal=f"Assist with tasks related to {employee.role}",
            backstory=self._create_backstory(employee),
            llm=f"{employee.llm_provider}/{employee.llm_model}",
            allow_delegation=True
        )
        return agent

    def create_crew(self, employees: list[AIEmployee]) -> Crew:
        """Create a Crew instance with the given employees."""
        agents = []
        for emp in employees:
            agent = self.create_agent(emp)
            agents.append(agent)

        crew = Crew(
            agents=agents,
            tasks=[],
            verbose=True,
            process=Process.hierarchical,
            manager_llm="openai/gpt-4.1"
        )

        return crew
    
    def create_task(self, meeting: Meeting, new_message: Message) -> Task:
        if not meeting or not new_message:
            raise ValueError("Meeting and message must be provided to create a task")
        
        task = Task(
            description=meeting.description,
            expected_output=new_message.content + "\nLimit the result to 900 characters.",
            markdown=True
        )

        return task
    
    def kickoff_crew(self, crew: Crew, task: Task) -> str:
        """Kick off the crew with the given task."""
        if not crew or not task:
            raise ValueError("Crew and task must be provided to kick off the crew")
        
        crew.tasks.append(task)
        crew_output = crew.kickoff()

        return crew_output.raw
    
# Global instance
crew_service = CrewService()
