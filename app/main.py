from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, Base, get_db
import app.api as api
from app.models import Task
from app.schemas import TaskCreate
from fastapi import HTTPException
import os
app = FastAPI()

@app.on_event("startup")
async def startup():
    # Delete DB file if exists
    if os.path.exists("test.db"):
        os.remove("test.db")
        print("Deleted existing test.db for a clean start.")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/tasks/")
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)):
    task = await api.create_task(db, task)
    return task

@app.get("/tasks/")
async def read_tasks(db: AsyncSession = Depends(get_db)):
    tasks = await api.get_tasks(db)
    return tasks

@app.get("/tasks/{task_id}")
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await api.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await api.update_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    task = await api.delete_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task