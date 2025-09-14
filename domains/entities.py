from calendar import c
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
        self.created_at = convert_to_datetime(self.created_at)
        self.updated_at = convert_to_datetime(self.updated_at)
        self.deadline = convert_to_datetime(self.deadline)

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
        self.created_at = convert_to_datetime(self.created_at)
        self.updated_at = convert_to_datetime(self.updated_at)
        self.deadline = convert_to_datetime(self.deadline)

        if self.created_at > self.updated_at:
            raise DateConstraintError("created_at cannot be later than updated_at")
            
    def assign_project(self, project: ProjectModel):
        self.project = project
        self.check_constraints()

    def check_constraints(self):
        project_deadline = convert_to_datetime(self.project.deadline) # type: ignore
        if self.deadline > project_deadline: # type: ignore
            raise DateConstraintError("Task deadline cannot exceed project's deadline")