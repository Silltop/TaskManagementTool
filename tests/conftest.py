import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, StaticPool, create_engine

from adapters.db_connector import create_db_and_tables, get_session
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
