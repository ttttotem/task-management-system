from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import engine, Base, get_db
import app.queries as queries
from app.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskFilter,
    Priority,
    Errors,
    TaskRead,
    TaskDeletedMessage,
)
from fastapi import HTTPException
from fastapi import Query
from typing import Optional

app = FastAPI(title="Task Management System")


@app.on_event("startup")
async def startup():
    print("start up")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.post("/tasks/")
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db)) -> TaskRead:
    """
    Create a task  

    **priority** - Values are (1 = High, 2 = Medium, 3 = Low)  
    **completed** - If not provided will default to False  
    """
    created_task = await queries.create_task(task, db)
    return created_task


@app.get("/tasks/")
async def read_tasks(
    page: int = Query(1),
    completed: Optional[bool] = Query(None),
    priority: Optional[Priority] = Query(None),
    search: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
) -> list[TaskRead]:
    """
    Get tasks with optional filtering  

    **page** - Used for pagination purposes, page-size is fixed at 20 tasks per page  
    **priority** - Values are (1 = High, 2 = Medium, 3 = Low)  
    **search** - Finds only tasks with exact matches (case insensitive) in either task title or task description  
    """
    task_filter = TaskFilter(
        completed=completed, priority=priority, search_terms=search, page=page
    )
    tasks = await queries.get_tasks(task_filter, db)
    return tasks


@app.get(
    "/tasks/{task_id}",
    responses={
        404: {"description": Errors.TASK_NOT_FOUND.value},
    },
)
async def read_task(task_id: int, db: AsyncSession = Depends(get_db)) -> TaskRead:
    """
    Get task by task id
    """
    task = await queries.get_task_by_id(task_id, db)
    if not task:
        raise HTTPException(status_code=404, detail=Errors.TASK_NOT_FOUND.value)
    return task


@app.put(
    "/tasks/{task_id}",
    responses={
        404: {"description": Errors.TASK_NOT_FOUND.value},
    },
)
async def update_task(
    task_id: int, task: TaskUpdate, db: AsyncSession = Depends(get_db)
) -> TaskRead:
    """
    Update a task  

    Returns the full resulting task object after the update is applied
    """
    updated_task = await queries.update_task(task_id, task, db)
    return updated_task


@app.delete(
    "/tasks/{task_id}",
    responses={
        404: {"description": Errors.TASK_NOT_FOUND.value},
    },
)
async def delete_task(
    task_id: int, db: AsyncSession = Depends(get_db)
) -> TaskDeletedMessage:
    """
    Deletes a specific task
    """
    task_deleted_message = await queries.delete_task(task_id, db)
    return task_deleted_message
