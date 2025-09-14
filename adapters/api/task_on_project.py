from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from adapters.api.projects import get_project_or_404
from adapters.api.tasks import get_task_or_404
from adapters.db_connector import get_session
from application.task_on_project import TaskOnProject
from domains.models import TaskModel

router = APIRouter(prefix="/projects")
task_on_project = TaskOnProject()
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/{project_id}/tasks/{task_id}/link", status_code=200)
def link_task_to_project(project_id: str, task_id: str, session: SessionDep):
    project = get_project_or_404(project_id, session)
    task = get_task_or_404(task_id, session)

    result = task_on_project.link_task_to_project(project, task, session)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to link task to project")
    return {"message": "Task linked to project"}


@router.delete("/{project_id}/tasks/{task_id}/unlink", status_code=200)
def unlink_task_from_project(project_id: str, task_id: str, session: SessionDep):
    project = get_project_or_404(project_id, session)
    task = get_task_or_404(task_id, session)

    result = task_on_project.unlink_task_from_project(project, task, session)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to unlink task from project")
    return {"message": "Task unlinked from project"}


@router.get("/{id}/tasks", response_model=list[TaskModel])
def get_project_tasks(id: str, session: SessionDep):
    project = get_project_or_404(id, session)
    tasks = task_on_project.get_project_tasks(project.id, session)
    return tasks
