from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Task
from app.database import engine, Base, get_db
import app.api as api
from app.schemas import TaskCreate, TaskUpdate, TaskFilter, Priority
from fastapi import HTTPException
from fastapi import Query
from typing import Optional
import os
app = FastAPI()
@app.on_event("startup")
async def startup():
    print("start up")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/tasks/")
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    """
    Create a task

    **priority** - Values are (1 = High, 2 = Medium, 3 = Low)  
    **completed** - If not provided will default to False
    """
    task = await api.create_task(db, task)
    return task

@app.get("/tasks/")
async def read_tasks(page: int = Query(1), completed: Optional[bool] = Query(None),priority: Optional[Priority] = Query(None),search: Optional[str] = Query(None),db: AsyncSession = Depends(get_db)):
    """
    Get tasks with optional filtering

    **page** - Used for pagination purposes, page-size is fixed
    **priority** - Values are (1 = High, 2 = Medium, 3 = Low)  
    **search** - Finds only tasks with exact matches (case insensitive) in either task title or task description
    """
    task_filter = TaskFilter(completed=completed, priority=priority, search_terms=search, page=page)
    tasks = await api.get_tasks(db, task_filter)
    return tasks

@app.get("/tasks/{task_id}")
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Get task by task id
    """
    task = await api.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db)):
    """
    Update a task

    Returns the full resulting task object after the update is applied
    """
    task = await api.update_task(db, task_id, task)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}"  ,responses={
        404: {"description": "Task not found"},
    })
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    """
    Deletes a specific task
    """
    task = await api.delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task