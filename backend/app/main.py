"""
FastAPI application initialization.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import employees, meetings, messages

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION
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
