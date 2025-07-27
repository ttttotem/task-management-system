from sqlalchemy.future import select
from sqlalchemy import delete, update
from app.models import Task
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

async def create_task(db, task_data):
    task = Task(title=task_data.title, description=task_data.description, priority=task_data.priority, due_date=task_data.due_date, completed=task_data.completed)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_tasks(db):
    result = await db.execute(select(Task))
    return result.scalars().all()

async def get_task_by_id(db, task_id):
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()

async def update_task(db, task_id, task_data):
    # Check if task exists
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    # Update fields dynamically from task_data
    update_data = task_data.dict(exclude_unset=True)
    if update_data:
        await db.execute(
            update(Task)
            .where(Task.id == task_id)
            .values(**update_data)
        )
        await db.commit()

    # Return updated task
    result = await db.execute(select(Task).where(Task.id == task_id))
    updated_task = result.scalars().first()
    return updated_task

async def delete_task(db, task_id):
    try:
        # Check if the task exists
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

        # Delete the task
        await db.execute(delete(Task).where(Task.id == task_id))
        await db.commit()
        return {"message": "Task deleted successfully"}
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting task")