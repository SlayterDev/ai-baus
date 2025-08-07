"""
FastAPI application initialization.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.routers import employees, meetings, messages
from app.database.init_db import create_tables, init_sample_data
from app.database.database import SessionLocal


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    print("Initializing database...")
    create_tables()
    
    # Initialize sample data
    db = SessionLocal()
    try:
        init_sample_data(db)
    finally:
        db.close()
    
    print("Database initialized successfully!")
    yield
    # Shutdown
    print("Application shutting down...")


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(employees.router)
app.include_router(meetings.router)
app.include_router(messages.router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": f"Welcome to the {settings.API_TITLE}!",
        "version": settings.API_VERSION
    }
