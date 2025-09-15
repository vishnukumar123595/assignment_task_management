# app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from typing import List, Optional

def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_tasks(db: Session, filters: dict) -> List[models.Task]:
    query = db.query(models.Task)
    if filters.get("status"):
        query = query.filter(models.Task.status == filters["status"])
    if filters.get("priority"):
        query = query.filter(models.Task.priority == filters["priority"])
    # Add more filtering logic for due_date ranges if needed
    return query.all()

def update_task(db: Session, task_id: int, task_data: schemas.TaskUpdate) -> Optional[models.Task]:
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        update_data = task_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_task, key, value)
        db.commit()
        db.refresh(db_task)
    return db_task

# ... Add delete_task and other helper functions

def delete_task(db: Session, task_id: Optional[int] = None, title: Optional[str] = None) -> bool:
    query = db.query(models.Task)
    
    if task_id:
        query = query.filter(models.Task.id == task_id)
    elif title:
        query = query.filter(models.Task.title.ilike(f"%{title}%"))

    task = query.first()
    if task:
        db.delete(task)
        db.commit()
        return True
    return False

def filter_tasks(db: Session, status: Optional[models.TaskStatus] = None, priority: Optional[models.TaskPriority] = None) -> List[models.Task]:
    query = db.query(models.Task)
    if status:
        query = query.filter(models.Task.status == status)
    if priority:
        query = query.filter(models.Task.priority == priority)
    return query.all()

