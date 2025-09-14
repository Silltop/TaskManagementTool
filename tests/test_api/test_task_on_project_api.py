from urllib import response
from urllib.parse import urlencode
import pytest
from unittest.mock import patch

BASE_URL = "/projects"
TASKS_URL = "/tasks"  # adjust if your tasks router uses a different prefix


def test_link_task_to_project(client, sample_project, sample_task):
    project_resp = client.post(BASE_URL + "/", json=sample_project)
    task_resp = client.post(TASKS_URL + "/", json=sample_task)
    project_id = project_resp.json()["id"]
    task_id = task_resp.json()["id"]
    response = client.post(f"{BASE_URL}/{project_id}/tasks/{task_id}/link")
    assert response.status_code == 200
    assert response.json() == {"message": "Task linked to project"}


def test_unlink_task_from_project(client, sample_project, task_related_to_project):
    project_resp = client.post(BASE_URL + "/", json=sample_project)
    task_resp = client.post(TASKS_URL + "/", json=task_related_to_project)
    project_id = project_resp.json()["id"]
    task_id = task_resp.json()["id"]

    response = client.delete(f"{BASE_URL}/{project_id}/tasks/{task_id}/unlink")
    assert response.status_code == 200
    assert response.json() == {"message": "Task unlinked from project"}


def test_get_project_tasks(client, sample_project, sample_task, task_related_to_project):
    project_resp = client.post(BASE_URL + "/", json=sample_project)
    project_id = project_resp.json()["id"]

    client.post(TASKS_URL + "/", json=sample_task)             # not linked
    linked_task = client.post(TASKS_URL + "/", json=task_related_to_project).json()

    response = client.get(f"{BASE_URL}/{project_id}/tasks")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == linked_task["id"]


def test_link_task_to_project_project_not_found(client, sample_task):
    task_resp = client.post(TASKS_URL + "/", json=sample_task)
    task_id = task_resp.json()["id"]

    response = client.post(f"{BASE_URL}/cfa85f64-1476-4562-b3fc-2c555f66afa6/tasks/{task_id}/link")
    assert response.status_code == 404


def test_link_task_to_project_task_not_found(client, sample_project):
    project_resp = client.post(BASE_URL + "/", json=sample_project)
    project_id = project_resp.json()["id"]

    response = client.post(f"{BASE_URL}/{project_id}/tasks/bfa85f64-1476-4562-b3fc-2c555f66afa6/link")
    assert response.status_code == 404


def test_unlink_task_from_project_project_not_found(client, sample_task):
    task_resp = client.post(TASKS_URL + "/", json=sample_task)
    task_id = task_resp.json()["id"]

    response = client.delete(f"{BASE_URL}/bfb85f64-1476-4562-b3fc-2c555f66afa6/tasks/{task_id}/unlink")
    assert response.status_code == 404


def test_unlink_task_from_project_task_not_found(client, sample_project):
    project_resp = client.post(BASE_URL + "/", json=sample_project)
    project_id = project_resp.json()["id"]

    response = client.delete(f"{BASE_URL}/{project_id}/tasks/bfa85f84-1476-4562-b3fc-2c555f66afa6/unlink")
    assert response.status_code == 404
