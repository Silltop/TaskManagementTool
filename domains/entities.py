from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union
from uuid import UUID

from domains.models import ProjectModel, TaskModel
from infrastructure.errors import DateConstraintError
from infrastructure.utils.converters import convert_to_datetime, convert_to_uuid


@dataclass
class ProjectEntity:
    id: Union[UUID, str]
    title: str
    deadline: Union[datetime, str]
    created_at: Union[datetime, str]
    updated_at: Union[datetime, str]
    completed: bool = False
    tasks: Optional[list[TaskModel]] = None

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = convert_to_uuid(self.id)
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(str(self.created_at).replace("Z", "+00:00"))
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(str(self.updated_at).replace("Z", "+00:00"))
        if isinstance(self.deadline, str):
            self.deadline = datetime.fromisoformat(str(self.deadline).replace("Z", "+00:00"))

        if self.created_at > self.updated_at:
            raise DateConstraintError("created_at cannot be later than updated_at")
        if self.tasks:
            for task in self.tasks:
                if task.deadline > self.deadline:
                    raise DateConstraintError("Task deadline cannot exceed project's deadline")


@dataclass
class TaskEntity:
    id: Union[UUID, str]
    title: str
    description: Optional[str]
    deadline: Union[datetime, str]
    completed: bool
    project_id: Optional[Union[UUID, str]]
    created_at: Union[datetime, str]
    updated_at: Union[datetime, str]
    project: Optional[ProjectModel] = None

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = convert_to_uuid(self.id)
        if self.project_id and isinstance(self.project_id, str):
            self.project_id = convert_to_uuid(self.project_id)
        if isinstance(self.created_at, str):
            self.created_at = convert_to_datetime(self.created_at)
        if isinstance(self.updated_at, str):
            self.updated_at = convert_to_datetime(self.updated_at)
        if isinstance(self.deadline, str):
            self.deadline = convert_to_datetime(self.deadline)

        if self.created_at > self.updated_at:
            raise DateConstraintError("created_at cannot be later than updated_at")
        if self.project:
            if self.deadline > self.project.deadline:
                raise DateConstraintError("Task deadline cannot exceed project's deadline")
