import pytest

BASE_URL = "/tasks"


@pytest.fixture
def sample_task():
    return {"id": "task_123", "title": "Test Task", "description": "A task for testing"}


def test_create_task(client, sample_task):
    response = client.post(BASE_URL + "/", json=sample_task)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_task["id"]
    assert data["title"] == sample_task["title"]


def test_create_task_conflict(client, sample_task):
    client.post(BASE_URL + "/", json=sample_task)
    response = client.post(BASE_URL + "/", json=sample_task)
    assert response.status_code == 409
    assert response.json()["detail"] == "Task with this ID already exists"


def test_list_tasks(client, sample_task):
    # Insert a task first
    client.post(BASE_URL + "/", json=sample_task)
    response = client.get(BASE_URL + "/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(t["id"] == sample_task["id"] for t in data)


def test_get_task(client, sample_task):
    client.post(BASE_URL + "/", json=sample_task)
    response = client.get(BASE_URL + f"/{sample_task['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_task["id"]


def test_get_task_not_found(client):
    response = client.get(BASE_URL + "/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task(client, sample_task):
    client.post(BASE_URL + "/", json=sample_task)
    updated = {**sample_task, "title": "Updated Task"}
    response = client.put(BASE_URL + f"/{sample_task['id']}", json=updated)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Task"


def test_update_task_not_found(client, sample_task):
    response = client.put(BASE_URL + "/nonexistent", json=sample_task)
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_delete_task(client, sample_task):
    client.post(BASE_URL + "/", json=sample_task)
    response = client.delete(BASE_URL + f"/{sample_task['id']}")
    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(BASE_URL + f"/{sample_task['id']}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete(BASE_URL + "/nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
