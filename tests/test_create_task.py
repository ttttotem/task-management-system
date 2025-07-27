from fastapi.testclient import TestClient
from app.main import app 
from app.schemas import TaskRead
from datetime import datetime
import pytest
client = TestClient(app)


@pytest.fixture
def valid_create_task():
    return {
    "title": "Task Title",
    "description": "Task Description",
    "priority": 1,
    "due_date": "2000-01-30T15:00:00",
    }

def test_create_task(valid_create_task):
    response = client.post("/tasks/", json=valid_create_task)
    assert response.status_code == 200
        
    task = TaskRead(**response.json())
    assert task.title == valid_create_task['title']
    assert task.description == valid_create_task['description']
    assert task.due_date == datetime.fromisoformat(valid_create_task['due_date'])
    assert task.priority == valid_create_task['priority']
    assert task.id
    assert not task.completed

def test_create_task_completed(valid_create_task):
    valid_create_task["completed"] = True
    response = client.post("/tasks/", json=valid_create_task)
    assert response.status_code == 200
        
    task = TaskRead(**response.json())
    assert task.title == valid_create_task['title']
    assert task.description == valid_create_task['description']
    assert task.due_date == datetime.fromisoformat(valid_create_task['due_date'])
    assert task.priority == valid_create_task['priority']
    assert task.id
    assert task.completed

def test_create_task_invalid_priority(valid_create_task):
    valid_create_task["priority"] = 4
    response = client.post("/tasks/", json=valid_create_task)
    assert response.status_code == 422

