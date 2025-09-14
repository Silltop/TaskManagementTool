BASE_URL = "/projects"


def test_create_project(client, sample_project):
    response = client.post(BASE_URL + "/", json=sample_project)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == sample_project["id"]


def test_get_project(client, sample_project):
    # First insert
    client.post(BASE_URL + "/", json=sample_project)

    response = client.get(BASE_URL + f"/{sample_project['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_project["id"]


def test_get_project_not_found(client):
    response = client.get(BASE_URL + "/3fa85f64-5717-4562-b3fc-2c963f66afa4")
    print(response.json())
    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_update_project(client, sample_project):
    client.post(BASE_URL + "/", json=sample_project)
    updated = {**sample_project, "title": "Updated Project"}
    response = client.put(BASE_URL + f"/{sample_project['id']}", json=updated)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Project"


def test_update_project_not_found(client, sample_project):
    response = client.put(BASE_URL + "/3fa85f64-5717-4562-b3fc-2c963f66afa4", json=sample_project)
    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_delete_project(client, sample_project):
    client.post(BASE_URL + "/", json=sample_project)
    response = client.delete(BASE_URL + f"/{sample_project['id']}")
    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(BASE_URL + f"/{sample_project['id']}")
    assert get_response.status_code == 404


def test_delete_project_not_found(client):
    response = client.delete(BASE_URL + "/3fa85f64-5717-4562-b3fc-2c963f66afa4")
    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_create_project_conflict(client, sample_project):
    client.post(BASE_URL + "/", json=sample_project)
    response = client.post(BASE_URL + "/", json=sample_project)
    assert response.status_code == 409
    assert response.json()["detail"] == "Project with this ID already exists"
