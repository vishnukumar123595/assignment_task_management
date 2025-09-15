# 🧠 AI Task Manager Agent

An intelligent task management system powered by FastAPI, LangChain, and a frontend built with React. Supports AI-driven task creation, updating, and filtering via WebSocket, and RESTful APIs for CRUD operations.

---

## 🚀 Features

- ✨ AI agent for interpreting and creating tasks from natural language
- 📋 REST API to create, list, update, and delete tasks
- 🔍 Filter tasks by `status` or `priority`
- 🧠 LangGraph + LangChain agent integration
- 🌐 WebSocket connection for real-time AI responses
- ⚛️ React-based frontend interface

---

## 📦 Tech Stack

### Backend:
- Python 3.11+
- FastAPI
- SQLAlchemy
- SQLite (default)
- LangChain + LangGraph
- Google Generative Language API
- WebSockets

### Frontend:
- React
- Tailwind CSS (if used)
- WebSocket client
- fetch (for API calls)

---

## 🛠️ Installation

### 🐍 Backend Setup

```bash
# 1. Clone the repo
git clone https://github.com/vishnukumar123595/Task_manager_agent.git
cd Task_manager_agent/backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Start FastAPI server
uvicorn main:app --reload

Visit backend docs at: http://127.0.0.1:8000/docs


cd ../frontend

# Install dependencies
npm install

# Start development server
npm start

Message - "Buy groceries tomorrow evening"

Method	Endpoint	Description
GET	/api/tasks/	List all tasks
POST	/api/tasks/	Create a new task
PUT	/api/tasks/{id}	Update a task by ID
DELETE	/api/tasks/{id}	Delete a task by ID
GET	/api/tasks/filter Filter tasks by status and priority.
