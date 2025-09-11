from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from adapters.api.projects import router
from adapters.db_connector import get_session
from application.project import Project
from application.task_on_project import TaskOnProject
from application.tasks import Task
from domains.models import TaskModel

SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/{project_id}/tasks/{task_id}/link", status_code=status.HTTP_200_OK)
def link_task_to_project(project_id: str, task_id: str, session: SessionDep):
    project = Project().get_project(project_id, session=session)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    task = Task().get_task(task_id, session=session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    result = TaskOnProject().link_task_to_project(project, task, session=session)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to link task to project")
    return {"message": "Task linked to project"}


@router.delete("/{project_id}/tasks/{task_id}/unlink", status_code=status.HTTP_200_OK)
def unlink_task_from_project(project_id: str, task_id: str, session: SessionDep):
    project = Project().get_project(project_id, session=session)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    task = Task().get_task(task_id, session=session)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    result = TaskOnProject().unlink_task_from_project(project, task, session=session)
    if not result:
        raise HTTPException(status_code=500, detail="Failed to unlink task from project")
    return {"message": "Task unlinked from project"}


@router.get("/{id}/tasks", response_model=list[Task])
def get_project_tasks(id: str, session: SessionDep) -> list[TaskModel] | None:
    tasks = TaskOnProject().get_project_tasks(id, session=session)
    if tasks is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return tasks
