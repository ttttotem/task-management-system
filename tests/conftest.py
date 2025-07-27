from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from fastapi.testclient import TestClient
from app.database import get_db, Base
import pytest
import asyncio

client = TestClient(app)
TEST_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(TEST_DATABASE_URL, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore


async def override_get_db():
    async with async_session() as db:
        yield db


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def create_test_database():
    async def init_db():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(init_db())
    yield


@pytest.fixture
def valid_create_task():
    return {
        "title": "Task Title",
        "description": "Task Description",
        "priority": 1,
        "due_date": "2000-01-30T15:00:00",
    }


@pytest.fixture
def valid_create_task_2():
    return {
        "title": "Task type 2",
        "description": "Task type 2 Description",
        "priority": 2,
        "due_date": "2020-01-30T15:00:00",
    }


@pytest.fixture
def populated_session(valid_create_task, valid_create_task_2, create_test_database):
    for _ in range(11):
        response = client.post("/tasks/", json=valid_create_task)
    for _ in range(12):
        response = client.post("/tasks/", json=valid_create_task_2)
    return None
