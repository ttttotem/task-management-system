from app.schemas import TaskRead
from datetime import datetime
from conftest import client


def test_create_task(valid_create_task):
    response = client.post("/tasks/", json=valid_create_task)
    assert response.status_code == 200

    task = TaskRead(**response.json())
    assert task.title == valid_create_task["title"]
    assert task.description == valid_create_task["description"]
    assert task.due_date == datetime.fromisoformat(valid_create_task["due_date"])
    assert task.priority == valid_create_task["priority"]
    assert task.id
    assert not task.completed


def test_create_task_completed(valid_create_task):
    valid_create_task["completed"] = True
    response = client.post("/tasks/", json=valid_create_task)
    assert response.status_code == 200

    task = TaskRead(**response.json())
    assert task.title == valid_create_task["title"]
    assert task.description == valid_create_task["description"]
    assert task.due_date == datetime.fromisoformat(valid_create_task["due_date"])
    assert task.priority == valid_create_task["priority"]
    assert task.id
    assert task.completed


def test_create_task_invalid_priority(valid_create_task):
    valid_create_task["priority"] = 4
    response = client.post("/tasks/", json=valid_create_task)
    assert response.status_code == 422
