import uuid
from typing import Optional, Protocol

from domains.entities import TaskEntity
from domains.models import TaskModel


class TaskPort(Protocol):
    def __init__(self) -> None:
        pass

    def list_tasks(self, session) -> Optional[list[TaskModel]]:
        pass

    def create_task(self, task: TaskEntity, session) -> Optional[TaskModel]:
        pass

    def update_task(self, id: uuid.UUID, task: TaskEntity, session) -> Optional[TaskModel]:
        pass

    def remove_task(self, id: uuid.UUID, session) -> bool:  # type: ignore
        pass

    def get_task(self, id: uuid.UUID, session) -> Optional[TaskModel]:
        pass
