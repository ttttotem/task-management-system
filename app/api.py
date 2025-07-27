from sqlalchemy.future import select
from app.models import Task

async def create_task(db, task_data):
    task = Task(title=task_data.title, description=task_data.description, priority=task_data.priority, due_date=task_data.due_date, completed=task_data.completed)
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task

async def get_tasks(db):
    result = await db.execute(select(Task))
    return result.scalars().all()

async def get_task_by_id(db):
    result = await db.execute(select(Task))
    return result.scalars().all()

async def update_task(db):
    pass

async def delete_task(db):
    pass