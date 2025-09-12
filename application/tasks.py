import uuid
from datetime import datetime, timedelta, timezone
from typing import Union

from sqlmodel import Session, select

from adapters.api.helpers import get_uuid
from application.project import ProjectService
from domains.entities import TaskEntity
from domains.models import TaskModel
from infrastructure.loggers import app_logger as logger
from ports.task_port import TaskPort


class TaskService(TaskPort):
    def list_tasks(self, session) -> list[TaskModel]:
        tasks = session.exec(select(TaskModel)).all()
        return list(tasks)

    def create_task(self, task: TaskEntity, session: Session) -> Union[TaskModel, None]:
        if task.project_id:
            task.project = ProjectService().get_project(get_uuid(task.project_id), session)
        existing_task = session.exec(select(TaskModel).where(TaskModel.id == task.id)).first()
        if existing_task:
            return None
        new_task = TaskModel(**task.__dict__)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task

    def update_task(self, id: uuid.UUID, task: TaskEntity, session: Session) -> Union[TaskModel, None]:
        existing_task = session.exec(select(TaskModel).where(TaskModel.id == id)).first()
        if not existing_task:
            return None
        was_completed = getattr(existing_task, "completed", False)
        for key, value in task.__dict__.items():
            if value is not None:
                setattr(existing_task, key, value)
        session.add(existing_task)
        session.commit()
        session.refresh(existing_task)
        if not was_completed and getattr(existing_task, "completed", False):
            logger.info(f"Task {existing_task.id} marked as completed.")
        return existing_task

    def remove_task(self, id: uuid.UUID, session: Session) -> bool:
        existing_task = session.exec(select(TaskModel).where(TaskModel.id == id)).first()
        if not existing_task:
            return False
        session.delete(existing_task)
        session.commit()
        return True

    def get_task(self, id: uuid.UUID, session: Session) -> Union[TaskModel, None]:
        task = session.exec(select(TaskModel).where(TaskModel.id == id)).first()
        return task

    def check_deadlines(self, session: Session, due: int) -> list[TaskModel]:
        now = datetime.now(timezone.utc)
        upcoming = now + timedelta(hours=due)
        tasks = session.exec(
            select(TaskModel).where(
                TaskModel.deadline is not None,
                not TaskModel.completed,
                TaskModel.deadline <= upcoming,
                TaskModel.deadline >= now,
            )
        ).all()
        return list(tasks)

    def complete_task(self, id: uuid.UUID, session: Session) -> TaskModel | None:
        task = self.get_task(id, session)
        if not task:
            return None
        task.completed = True
        session.add(task)
        session.commit()
        session.refresh(task)
        logger.info(f"Task {task.id} marked as completed.")
        return task
