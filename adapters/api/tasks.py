import logging
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from adapters.db_connector import get_session
from application.tasks import Task
from domains.entities import TaskEntity
from domains.models import TaskModel

router = APIRouter(prefix="/tasks")
SessionDep = Annotated[Session, Depends(get_session)]


@router.get("/")
def list_tasks(session: SessionDep) -> list[TaskModel]:
    tasks = Task().list_tasks(session=session)
    return tasks


@router.post("/")
def create_task(task: TaskEntity, session: SessionDep) -> Optional[TaskModel]:
    new_task = Task().create_task(task, session)
    if not new_task:
        raise HTTPException(status_code=409, detail="Task with this ID already exists")
    return new_task


@router.put("/{id}")
def update_task(id: str, task: TaskEntity, session: SessionDep) -> TaskModel:
    updated_task = Task().update_task(id, task, session)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{id}", status_code=204)
def delete_task(id: str, session: SessionDep) -> None:
    status = Task().remove_task(id, session)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return


@router.get("/{id}")
def get_task(id: str, session: SessionDep) -> TaskModel:
    task = Task().get_task(id, session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


# TODO patch missing
