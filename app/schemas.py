from pydantic import BaseModel
import enum
from datetime import datetime

class Priority(enum.IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    priority: Priority
    due_date: datetime
    completed: bool | None = None

class TaskRead(TaskCreate):
    id: int

    class Config:
        orm_mode = True
