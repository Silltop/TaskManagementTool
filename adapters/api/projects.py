from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from adapters.db_connector import get_session
from application.project import Project
from domains.entities import ProjectEntity
from domains.models import ProjectModel

router = APIRouter(prefix="/projects")
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/{id}")
def get_project(id: str, session: SessionDep) -> ProjectModel:
    project = Project().get_project(id, session)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectEntity, session: SessionDep) -> ProjectModel:
    new_project = Project().create_project(project, session)
    if not new_project:
        raise HTTPException(status_code=409, detail="Project with this ID already exists")
    return new_project


@router.put("/{id}")
def update_project(id: str, project: ProjectEntity, session: SessionDep) -> ProjectModel:
    updated_project = Project().update_project(id, project, session)
    if not updated_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return updated_project


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: str, session: SessionDep) -> None:
    status = Project().remove_project(id, session)
    if not status:
        raise HTTPException(status_code=404, detail="Project not found")
    return
