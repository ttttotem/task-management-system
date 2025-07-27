from conftest import client
from app.schemas import TaskRead


def test_get_tasks_empty():
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks(populated_session):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert len(response.json()) == 20


def test_get_tasks_page_final(populated_session):
    response = client.get("/tasks/", params={"page": 2})
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_tasks_page_above_max(populated_session):
    response = client.get("/tasks/", params={"page": 200})
    assert response.status_code == 200
    assert response.json() == []


def test_get_tasks_filtering(populated_session):
    response = client.get("/tasks/", params={"priority": 2})
    assert response.status_code == 200
    assert len(response.json()) == 12


def test_get_task_by_id(populated_session):
    test_id = 7
    response = client.get(f"/tasks/{test_id}")
    assert response.status_code == 200
    task = TaskRead(**response.json())
    assert task.id == test_id


def test_get_task_by_missing_id(populated_session):
    test_id = 40
    response = client.get(f"/tasks/{test_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
