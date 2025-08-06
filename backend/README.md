# AI Boss Backend

A modular FastAPI application for managing AI employees and meetings.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration settings
│   ├── models/                 # Pydantic models
│   │   ├── __init__.py
│   │   ├── employee.py         # Employee models
│   │   ├── meeting.py          # Meeting models
│   │   └── message.py          # Message models
│   ├── services/               # Business logic
│   │   ├── __init__.py
│   │   ├── llm_service.py      # LLM management
│   │   ├── employee_service.py # Employee business logic
│   │   ├── meeting_service.py  # Meeting business logic
│   │   └── message_service.py  # Message business logic
│   ├── routers/                # API endpoints
│   │   ├── __init__.py
│   │   ├── employees.py        # Employee endpoints
│   │   ├── meetings.py         # Meeting endpoints
│   │   └── messages.py         # Message endpoints
│   └── database/               # Data storage
│       ├── __init__.py
│       └── memory_store.py     # In-memory database simulation
├── Dockerfile
├── requirements.txt
├── run.py                      # Application entry point
└── README.md
```

## Features

- **Modular Architecture**: Clean separation of concerns with dedicated modules for models, services, and routes
- **AI Employee Management**: Create and manage AI employees with different personalities and expertise
- **Meeting System**: Organize AI employees into meetings for conversations
- **LLM Integration**: Support for OpenAI and Anthropic models
- **RESTful API**: Well-structured REST endpoints with proper HTTP methods

## Running the Application

### Development
```bash
python run.py
```

### Production with Docker
```bash
docker build -t ai-boss-backend .
docker run -p 8000:8000 ai-boss-backend
```

## Environment Variables

Create a `.env` file in the backend directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

## API Endpoints

### Employees
- `POST /employees` - Create a new AI employee
- `GET /employees` - Get all employees
- `GET /employees/{employee_id}` - Get a specific employee
- `DELETE /employees/{employee_id}` - Delete an employee

### Meetings
- `POST /meetings` - Create a new meeting
- `GET /meetings` - Get all meetings  
- `GET /meetings/{meeting_id}` - Get a specific meeting

### Messages
- `POST /meetings/{meeting_id}/messages` - Send a message to a meeting
- `POST /meetings/{meeting_id}/messages/{employee_id}/respond` - Generate AI employee response
- `GET /meetings/{meeting_id}/messages` - Get all messages in a meeting

## Architecture Benefits

1. **Separation of Concerns**: Each module has a specific responsibility
2. **Testability**: Services can be easily unit tested
3. **Maintainability**: Changes to business logic don't affect API routes
4. **Scalability**: Easy to add new features and endpoints
5. **Configuration Management**: Centralized settings in config.py
6. **Database Abstraction**: Easy to switch from in-memory to persistent storage

## Next Steps

- Replace in-memory storage with a proper database (PostgreSQL, MongoDB, etc.)
- Add authentication and authorization
- Implement proper logging
- Add comprehensive error handling
- Add unit and integration tests
- Add API documentation with OpenAPI/Swagger
