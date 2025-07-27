from pydantic import BaseModel
import enum
from datetime import datetime
from typing import Optional

class Priority(enum.IntEnum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Priority
    due_date: datetime
    completed: Optional[bool] = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    due_date: Optional[datetime] = None
    completed: Optional[bool] = None 

class TaskFilter(BaseModel):
    completed: Optional[bool] = None
    priority: Optional[Priority] = None
    search_terms: Optional[str] = None
    page: int = 1


class TaskRead(TaskCreate):
    id: int

    class Config:
        orm_mode = True
