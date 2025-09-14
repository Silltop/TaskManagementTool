import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from adapters.db_connector import get_session
from domains.entities import ProjectEntity, TaskEntity  # noqa: F401
from main import app  # Adjust the import based on your project structure


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


# Override the get_session dependency so FastAPI uses our test session
@pytest.fixture
def client(session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override  # noqa: F821
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def sample_project():
    return {
        "id": "afa85f64-5717-4562-b3fc-2c963f66afa6",
        "title": "string",
        "deadline": "2025-09-12T17:28:37.590Z",
        "completed": False,
        "created_at": "2025-09-12T17:28:37.590Z",
        "updated_at": "2025-09-12T17:28:37.590Z",
    }


@pytest.fixture
def sample_task():
    return {
        "id": "bfa85f64-1476-4562-b3fc-2c555f66afa6",
        "title": "string",
        "description": "string",
        "deadline": "2025-09-12T19:23:10.513Z",
        "completed": False,
        "project_id": None,
        "created_at": "2025-09-12T19:23:10.513Z",
        "updated_at": "2025-09-12T19:23:10.513Z",
    }


@pytest.fixture
def task_related_to_project():
    return {
        "id": "3fa85f64-5717-4562-b3fc-2c444f66afa6",
        "title": "string",
        "description": "string",
        "deadline": "2025-09-13T19:23:10.513Z",
        "completed": False,
        "project_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "created_at": "2025-09-12T19:23:10.513Z",
        "updated_at": "2025-09-12T19:23:10.513Z",
    }
