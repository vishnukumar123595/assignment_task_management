
# app/tools.py

from langchain_core.tools import tool
from typing import Optional, List
from datetime import datetime
import dateparser

from . import crud, schemas
from .database import SessionLocal
from .models import TaskStatus, TaskPriority

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@tool
def create_task(
    title: str,
    description: Optional[str] = None,
    due_date: Optional[str] = None,
    priority: Optional[str] = "medium"
) -> dict:
    """Creates a new task with title and optional description, due date, and priority."""
    db_session = next(get_db())

    try:
        parsed_due_date = dateparser.parse(due_date) if due_date else None
        priority_enum = TaskPriority(priority.lower())
    except ValueError:
        return {"type": "error", "message": f"Invalid priority: {priority}"}

    task_create = schemas.TaskCreate(
        title=title,
        description=description,
        due_date=parsed_due_date,
        priority=priority_enum
    )
    task = crud.create_task(db=db_session, task=task_create)
    return {
        "type": "info",
        "message": f"✅ Task '{task.title}' created successfully with ID {task.id}."
    }


@tool
def list_tasks() -> dict:
    """Lists all tasks."""
    db_session = next(get_db())
    tasks = crud.get_tasks(db=db_session, filters={})
    return {
        "type": "task_list",
        "tasks": [schemas.Task.from_orm(t).dict() for t in tasks]
    }


@tool
def filter_tasks(
    status: Optional[str] = None,
    priority: Optional[str] = None
) -> dict:
    """Filters tasks by status or priority."""
    db_session = next(get_db())

    filters = {}

    if status:
        try:
            filters["status"] = TaskStatus(status.lower())
        except ValueError:
            return {"type": "error", "message": f"Invalid status: {status}"}

    if priority:
        try:
            filters["priority"] = TaskPriority(priority.lower())
        except ValueError:
            return {"type": "error", "message": f"Invalid priority: {priority}"}

    tasks = crud.get_tasks(db=db_session, filters=filters)
    return {
        "type": "task_list",
        "tasks": [schemas.Task.from_orm(t).dict() for t in tasks]
    }


@tool
def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    due_date: Optional[str] = None,
    priority: Optional[str] = None
) -> dict:
    """Updates a task by ID. Fields you can update: title, description, status, due_date, priority."""
    db_session = next(get_db())

    try:
        task_update = schemas.TaskUpdate(
            title=title,
            description=description,
            status=TaskStatus(status.lower()) if status else None,
            due_date=dateparser.parse(due_date) if due_date else None,
            priority=TaskPriority(priority.lower()) if priority else None,
        )
    except ValueError as e:
        return {"type": "error", "message": f"Invalid field: {str(e)}"}

    updated = crud.update_task(db=db_session, task_id=task_id, task_data=task_update)
    if updated:
        return {"type": "info", "message": f"✅ Task {task_id} updated successfully."}
    return {"type": "error", "message": f"❌ Task with ID {task_id} not found."}


@tool
def delete_task(
    task_id: Optional[int] = None,
    title: Optional[str] = None
) -> dict:
    """Deletes a task by ID or matching title. Provide either task_id or title."""
    db_session = next(get_db())

    if not task_id and not title:
        return {"type": "error", "message": "You must provide either a task ID or a title to delete."}

    deleted = crud.delete_task(db=db_session, task_id=task_id, title=title)
    if deleted:
        return {"type": "info", "message": "🗑️ Task successfully deleted."}
    else:
        return {"type": "error", "message": "Task not found."}


# Executor class for LangGraph
class ToolExecutor:
    def __init__(self, tools):
        self.tools = {tool.name: tool for tool in tools}

    def batch(self, tool_calls):
        results = []
        for call in tool_calls:
            tool_name = getattr(call, "tool_name", None)
            args = getattr(call, "args", [])
            kwargs = getattr(call, "kwargs", {})

            tool_func = self.tools.get(tool_name)
            if not tool_func:
                results.append({
                    "type": "error",
                    "message": f"Tool '{tool_name}' not found"
                })
                continue

            try:
                result = tool_func(*args, **kwargs)
                results.append(result)
            except Exception as e:
                results.append({
                    "type": "error",
                    "message": f"Error executing tool '{tool_name}': {str(e)}"
                })
        return results
