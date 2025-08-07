#!/usr/bin/env python3
"""
Database setup script for the AI Boss application.
"""
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine, text
from app.config import settings
from app.database.init_db import create_tables, init_sample_data
from app.database.database import SessionLocal


def check_database_connection():
    """Check if we can connect to the database."""
    try:
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def setup_database():
    """Set up the database with tables and sample data."""
    if not check_database_connection():
        return False
    
    try:
        print("Creating database tables...")
        create_tables()
        print("✅ Tables created successfully!")
        
        print("Initializing sample data...")
        db = SessionLocal()
        try:
            init_sample_data(db)
        finally:
            db.close()
        print("✅ Sample data initialized successfully!")
        
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Setting up AI Boss database...")
    
    if setup_database():
        print("🎉 Database setup completed successfully!")
    else:
        print("💥 Database setup failed!")
        sys.exit(1)
