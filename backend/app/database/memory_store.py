"""
In-memory database simulation for the AI Boss application.
This will be replaced with a proper database in production.
"""
from datetime import datetime
from app.models.employee import AIEmployee

# In-memory database simulation
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
