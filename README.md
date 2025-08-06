# AI Employee Manager - POC

A proof-of-concept application for managing AI employees and holding meetings with them.

## Features

- ✨ Create AI Employees with custom personalities and expertise
- 🤖 Support for OpenAI and Anthropic models (BYOK - Bring Your Own Key)
- 💬 Hold multi-agent meetings where AI employees can interact
- 🎯 Role-based AI personalities (Project Manager, Researcher, Developer, etc.)
- 🐳 Docker-based deployment

## Quick Start

### Prerequisites

- Docker and Docker Compose
- API keys for OpenAI and/or Anthropic

### Setup

1. **Clone and setup environment:**
   ```bash
   git clone <your-repo>
   cd ai-employee-manager
   cp .env.example .env
   ```

2. **Add your API keys to `.env`:**
   ```
   OPENAI_API_KEY=your_openai_key_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   ```

3. **Start the application:**
   ```bash
   docker-compose up -d
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

### Usage

1. **Create AI Employees:**
   - Click "Create New Employee"
   - Fill in name, role, personality, and expertise
   - Choose your preferred LLM provider and model

2. **Start a Meeting:**
   - Create a meeting and select 2+ employees
   - Join the meeting to start conversations
   - Request responses from specific employees
   - Have natural conversations with your AI team

### Project Structure

```
ai-employee-manager/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container
├── frontend/
│   ├── src/
│   │   ├── App.js          # React application
│   │   └── App.css         # Styling
│   ├── package.json        # Node dependencies
│   └── Dockerfile          # Frontend container
├── docker-compose.yml      # Container orchestration
└── .env.example           # Environment template
```

### API Endpoints

- `GET /employees` - List all employees
- `POST /employees` - Create new employee
- `GET /meetings` - List all meetings
- `POST /meetings` - Create new meeting
- `POST /meetings/{id}/messages` - Send message
- `POST /meetings/{id}/messages/{employee_id}/respond` - Get AI response

### Development

For development with hot-reload:

```bash
# Backend (Python)
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (React)
cd frontend
npm install
npm start
```
