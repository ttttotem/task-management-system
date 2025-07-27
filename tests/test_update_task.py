from app.schemas import TaskRead
from conftest import client


def test_update_task(populated_session, valid_create_task):
    response = client.put("/tasks/1", json={"priority": 2})
    assert response.status_code == 200
    task = TaskRead(**response.json())
    assert task.priority == 2


def test_update_task_empty(populated_session, valid_create_task):
    response = client.put("/tasks/1")
    assert response.status_code == 422


def test_update_priority_outside_valid_values(populated_session, valid_create_task):
    response = client.put("/tasks/1", json={"priority": 4})
    assert response.status_code == 422


def test_update_missing_id(populated_session, valid_create_task):
    response = client.put("/tasks/200", json={"priority": 3})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
