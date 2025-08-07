# Database Setup

This document explains how to set up PostgreSQL persistence for the AI Boss backend.

## Prerequisites

- PostgreSQL 15+ installed locally OR Docker Compose for containerized setup
- Python virtual environment with dependencies installed

## Environment Variables

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Required variables:
- `DATABASE_URL`: PostgreSQL connection string
- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key

## Setup Options

### Option 1: Using Docker Compose (Recommended)

1. Start all services including PostgreSQL:
```bash
docker-compose up -d
```

This will:
- Start PostgreSQL container with the `ai_boss` database
- Start the backend service with automatic database initialization
- Start the frontend service

### Option 2: Local PostgreSQL

1. Start PostgreSQL locally and create the database:
```sql
CREATE DATABASE ai_boss;
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run database setup:
```bash
python setup_db.py
```

4. Start the application:
```bash
python run.py
```

## Database Migrations

This project uses Alembic for database migrations.

### Generate a new migration:
```bash
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations:
```bash
alembic upgrade head
```

### Check migration status:
```bash
alembic current
alembic history
```

## Database Schema

The application uses three main tables:

### Employees
- `id`: UUID primary key
- `name`: Employee name (max 100 chars)
- `role`: Job role (max 100 chars)
- `personality`: Personality description (max 500 chars)
- `expertise`: JSON array of expertise areas
- `llm_provider`: AI provider ("openai" or "anthropic")
- `llm_model`: Model name
- `system_prompt`: Optional custom system prompt
- `created_at`: Timestamp
- `is_active`: Soft delete flag

### Meetings
- `id`: UUID primary key
- `title`: Meeting title (max 200 chars)
- `description`: Optional description
- `employee_ids`: JSON array of participant employee IDs
- `created_at`: Timestamp
- `is_active`: Soft delete flag

### Messages
- `id`: UUID primary key
- `meeting_id`: Foreign key to meetings table
- `content`: Message content (max 1000 chars)
- `sender_type`: "user" or "employee"
- `sender_id`: Foreign key to employees table (nullable for user messages)
- `sender_name`: Display name of sender
- `timestamp`: Message timestamp

## Troubleshooting

### Connection Issues
- Ensure PostgreSQL is running on the specified host/port
- Check your `DATABASE_URL` format: `postgresql://user:password@host:port/database`
- Verify database credentials and that the database exists

### Migration Issues
- Make sure all model imports are working in `alembic/env.py`
- Check that `target_metadata` is set correctly
- Ensure the database is accessible when running migrations

### Sample Data
The application automatically creates two sample AI employees:
- **Dinkleberg**: Project Manager with butt-kissing personality
- **McStuffins**: Software Engineer with nihilistic personality

You can modify or add more sample data in `app/database/init_db.py`.
