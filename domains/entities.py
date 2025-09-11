import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union
from uuid import UUID


@dataclass
class TaskEntity:
    id: Union[UUID, str]
    title: str
    description: Optional[str]
    deadline: datetime
    completed: bool
    project_id: Optional[int]
    created_at: Union[datetime, str]
    updated_at: Union[datetime, str]

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = uuid.UUID(str(self.id))
        # additional checks required to handle different types of date
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(str(self.created_at).replace("Z", "+00:00"))
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(str(self.created_at).replace("Z", "+00:00"))


# note common fields could be extracted or metadata could be used


@dataclass
class ProjectEntity:
    id: Union[UUID, str]
    title: str
    deadline: Union[datetime, str]
    created_at: Union[datetime, str]
    updated_at: Union[datetime, str]
    completed: bool = False

    def __post_init__(self):
        if isinstance(self.id, str):
            self.id = uuid.UUID(self.id)
        if isinstance(self.created_at, str):
            self.created_at = datetime.fromisoformat(str(self.created_at).replace("Z", "+00:00"))
        if isinstance(self.updated_at, str):
            self.updated_at = datetime.fromisoformat(str(self.updated_at).replace("Z", "+00:00"))
        if isinstance(self.deadline, str):
            self.deadline = datetime.fromisoformat(str(self.deadline).replace("Z", "+00:00"))
