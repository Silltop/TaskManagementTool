import uuid
from typing import Annotated, Optional

from fastapi import Depends
from pytest import Session
from sqlmodel import select

from adapters.db_connector import get_session
from application.project import ProjectService
from domains.models import ProjectModel, TaskModel

SessionDep = Annotated[Session, Depends(get_session)]

class TaskOnProject:
    def link_task_to_project(self, project: ProjectModel, task: TaskModel, session: Session) -> bool:
        if task.project_id == project.id:
            return True  # Task is already linked to the project
        task.project_id = project.id
        session.add(task)
        session.commit()
        return True

    def unlink_task_from_project(self, project: ProjectModel, task: TaskModel, session: Session) -> bool:
        if task.project_id != project.id:
            return False  # Task is not linked to the project
        task.project_id = None
        session.add(task)
        session.commit()
        return True

    def get_project_tasks(self, project_id: uuid.UUID, session: Session) -> Optional[list[TaskModel]]:
        project = ProjectService().get_project(project_id, session=session)
        if not project:
            return None
        tasks = session.exec(select(TaskModel).where(TaskModel.project_id == uuid.UUID(str(project.id)))).all()
        tasks = list(tasks)  # should be paginated in a real-world scenario
        return tasks
