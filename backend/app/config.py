"""
Configuration settings for the AI Boss application.
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Configuration
    API_TITLE = "AI Boss Backend"
    API_VERSION = "0.1.0"
    
    # CORS Configuration
    CORS_ORIGINS = ["http://localhost:3000"]
    
    # Database Configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/ai_boss")
    
    # LLM API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = 8000

settings = Settings()
