# app/api/tasks.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[schemas.Task])
def read_tasks(
    status: Optional[models.TaskStatus] = Query(None),
    priority: Optional[models.TaskPriority] = Query(None),
    db: Session = Depends(get_db)
):
    filters = {}
    if status:
        filters["status"] = status
    if priority:
        filters["priority"] = priority
    tasks = crud.get_tasks(db, filters)
    return tasks

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task)

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id, task_update)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    success = crud.delete_task(db, task_id=task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted successfully"}


# ✅ New filter route
@router.get("/filter", response_model=List[schemas.Task])
def filter_tasks_api(
    status: Optional[models.TaskStatus] = None,
    priority: Optional[models.TaskPriority] = None,
    db: Session = Depends(get_db)
):
    """
    Filter tasks by status and/or priority.

    Examples:
    - /api/filter?status=todo
    - /api/filter?priority=high
    - /api/filter?status=done&priority=low
    """
    return crud.filter_tasks(db=db, status=status, priority=priority)
