from conftest import client


def test_delete_task(populated_session, valid_create_task):
    test_id = 1
    response = client.delete(f"/tasks/{test_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted successfully."}

    # Try get the task to make sure it was deleted
    response = client.get(f"/tasks/{test_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}


def test_delete_task_bad_id(populated_session, valid_create_task):
    response = client.delete("/tasks/a")
    assert response.status_code == 422


def test_delete_missing_id(populated_session, valid_create_task):
    response = client.delete("/tasks/400")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}
