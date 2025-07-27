from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from datetime import datetime
from app.schemas import Priority
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(SQLEnum(Priority), nullable=False)
    due_date = Column(DateTime, nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
