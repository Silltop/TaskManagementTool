import pytest

BASE_URL = "/tasks"


@pytest.fixture
def sample_task():
    return {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "title": "string",
        "description": "string",
        "deadline": "2025-09-12T19:23:10.513Z",
        "completed": False,
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2025-09-12T19:23:10.513Z",
        "updated_at": "2025-09-12T19:23:10.513Z",
    }


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
    response = client.get(BASE_URL + "/3Da85f64-5717-4562-b3fc-2c963f66afa6")
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
    response = client.put(BASE_URL + "/3Da85f64-5717-4562-b3fc-2c963f66afa6", json=sample_task)
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
    response = client.delete(BASE_URL + "/3fa85f22-5717-4562-b3fc-2c963f66afa6")
    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"
