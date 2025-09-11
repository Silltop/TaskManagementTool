import uuid
from typing import Union

from sqlmodel import Session, select

from domains.entities import TaskEntity
from domains.models import TaskModel
from ports.task_port import TaskPort


class Task(TaskPort):
    def __init__(self):
        pass

    def list_tasks(self, session) -> list[TaskModel]:
        tasks = session.exec(select(TaskModel)).all()
        return tasks

    def create_task(self, task: TaskEntity, session: Session) -> Union[TaskModel, None]:
        existing_task = session.exec(select(TaskModel).where(TaskModel.id == task.id)).first()
        if existing_task:
            return None
        new_task = TaskModel(**task.__dict__)
        session.add(new_task)
        session.commit()
        session.refresh(new_task)
        return new_task

    def update_task(self, id: str, task: TaskEntity, session: Session) -> Union[TaskModel, None]:
        existing_task = session.exec(select(TaskModel).where(TaskModel.id == uuid.UUID(str(id)))).first()
        if not existing_task:
            return None
        for key, value in task.__dict__.items():
            if value is not None:
                setattr(existing_task, key, value)
        session.add(existing_task)
        session.commit()
        session.refresh(existing_task)
        return existing_task

    def remove_task(self, id: str, session: Session) -> bool:
        existing_task = session.exec(select(TaskModel).where(TaskModel.id == uuid.UUID(str(id)))).first()
        if not existing_task:
            return False
        session.delete(existing_task)
        session.commit()
        return True

    def get_task(self, id: str, session: Session) -> Union[TaskModel, None]:
        task = session.exec(select(TaskModel).where(TaskModel.id == uuid.UUID(str(id)))).first()
        return task
