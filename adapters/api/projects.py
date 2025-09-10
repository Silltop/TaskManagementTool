from typing import List

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from domains.models import Project, Task

router = APIRouter(prefix="/projects")


@router.get("/", response_model=list[Project])
def get_projects():
    return list(projects.values())


@router.get("/{id}", response_model=Project)
def get_project(id: int):
    project = projects.get(id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
def create_project(project: ProjectCreate):
    new_id = max(projects.keys(), default=0) + 1
    new_project = Project(id=new_id, **project.dict())
    projects[new_id] = new_project
    project_tasks[new_id] = []
    return new_project


@router.put("/{id}", response_model=Project)
def update_project(id: int, project: ProjectUpdate):
    existing = projects.get(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Project not found")
    update_data = project.dict(exclude_unset=True)
    updated = existing.copy(update=update_data)
    projects[id] = updated
    return updated


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(id: int):
    if id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    del projects[id]
    project_tasks.pop(id, None)
    return


@router.post("/{project_id}/tasks/{task_id}/link", status_code=status.HTTP_200_OK)
def link_task_to_project(project_id: int, task_id: int):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_id not in project_tasks.get(project_id, []):
        project_tasks[project_id].append(task_id)
    return {"message": "Task linked to project"}


@router.delete("/{project_id}/tasks/{task_id}/unlink", status_code=status.HTTP_200_OK)
def unlink_task_from_project(project_id: int, task_id: int):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_id in project_tasks.get(project_id, []):
        project_tasks[project_id].remove(task_id)
    return {"message": "Task unlinked from project"}


@router.get("/{id}/tasks", response_model=list[Task])
def get_project_tasks(id: int):
    if id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    task_ids = project_tasks.get(id, [])
    return [tasks[tid] for tid in task_ids if tid in tasks]
