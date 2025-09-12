from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from adapters.api.helpers import get_uuid
from adapters.db_connector import get_session
from application.tasks import TaskService
from domains.entities import TaskEntity
from domains.models import TaskModel

router = APIRouter(prefix="/tasks")
SessionDep = Annotated[Session, Depends(get_session)]

task_service = TaskService()


def get_task_or_404(task_id: str, session: Session) -> TaskModel:
    task = task_service.get_task(get_uuid(task_id), session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/")
def list_tasks(session: SessionDep) -> list[TaskModel]:
    tasks = task_service.list_tasks(session=session)
    return tasks


@router.post("/")
def create_task(task: TaskEntity, session: SessionDep) -> Optional[TaskModel]:
    new_task = task_service.create_task(task, session)
    if not new_task:
        raise HTTPException(status_code=409, detail="Task with this ID already exists")
    return new_task


@router.put("/{id}")
def update_task(id: str, task: TaskEntity, session: SessionDep) -> TaskModel:
    updated_task = task_service.update_task(get_uuid(id), task, session)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{id}", status_code=204)
def delete_task(id: str, session: SessionDep) -> None:
    status = task_service.remove_task(get_uuid(id), session)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return


@router.get("/{id}")
def get_task(id: str, session: SessionDep) -> TaskModel:
    return get_task_or_404(id, session)


@router.patch("/{id}/complete")
def complete_task(id: str, session: SessionDep):
    task = task_service.complete_task(get_uuid(id), session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
