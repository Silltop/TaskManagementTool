from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from adapters.api.helpers import get_uuid
from adapters.db_connector import get_session
from application.project import ProjectService
from domains.entities import ProjectEntity
from domains.models import ProjectModel

router = APIRouter(prefix="/projects")
SessionDep = Annotated[Session, Depends(get_session)]

project_service = ProjectService()


def get_project_or_404(project_id: str, session: Session) -> ProjectModel:
    project = project_service.get_project(get_uuid(project_id), session)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/{id}")
def get_project(id: str, session: SessionDep) -> ProjectModel:
    return get_project_or_404(id, session)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectEntity, session: SessionDep) -> ProjectModel:
    new_project = project_service.create_project(project, session)
    if not new_project:
        raise HTTPException(status_code=409, detail="Project with this ID already exists")
    return new_project


@router.put("/{id}")
def update_project(id: str, project: ProjectEntity, session: SessionDep) -> ProjectModel:
    updated_project = project_service.update_project(get_uuid(id), project, session)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: str, session: SessionDep) -> None:
    status = project_service.remove_project(get_uuid(id), session)
    if not status:
        raise HTTPException(status_code=404, detail="Project not found")
    return
