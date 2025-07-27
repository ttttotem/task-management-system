from sqlalchemy.future import select
from sqlalchemy import delete, update
from app.models import Task
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas import TaskCreate, TaskUpdate, TaskFilter, TaskRead, TaskDeletedMessage

PAGE_SIZE = 20


async def create_task(task_data: TaskCreate, db: AsyncSession) -> TaskRead:
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        completed=task_data.completed,
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task


async def get_tasks(task_filter: TaskFilter, db: AsyncSession) -> list[TaskRead]:
    query = select(Task)

    if task_filter.completed is not None:
        query = query.where(Task.completed == task_filter.completed)

    if task_filter.priority is not None:
        query = query.where(Task.priority == task_filter.priority)

    if task_filter.search_terms is not None:
        search_term = f"%{task_filter.search_terms.lower()}%"
        query = query.where(
            or_(Task.title.ilike(search_term), Task.description.ilike(search_term))
        )

    # Apply LIMIT/OFFSET based on fixed PAGE_SIZE
    offset = (task_filter.page - 1) * PAGE_SIZE
    paginated_query = query.limit(PAGE_SIZE).offset(offset)

    result = await db.execute(paginated_query)
    return result.scalars().all()  # type: ignore


async def get_task_by_id(task_id: int, db: AsyncSession) -> TaskRead:
    result = await db.execute(select(Task).where(Task.id == task_id))
    return result.scalars().first()  # type: ignore


async def update_task(
    task_id: int, task_data: TaskUpdate, db: AsyncSession
) -> TaskRead:
    # Check if task exists
    result = await db.execute(select(Task).where(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )

    # Update fields using task_data
    update_data = task_data.dict(exclude_unset=True)
    if update_data:
        await db.execute(update(Task).where(Task.id == task_id).values(**update_data))
        await db.commit()

    # Return updated task
    return await get_task_by_id(task_id, db)


async def delete_task(task_id: int, db: AsyncSession) -> TaskDeletedMessage:
    try:
        # Check if the task exists
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )

        # Delete the task
        await db.execute(delete(Task).where(Task.id == task_id))
        await db.commit()
        return TaskDeletedMessage()
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting task",
        )
