from typing import Optional, Protocol

from domains.entities import ProjectEntity
from domains.models import ProjectModel


class ProjectPort(Protocol):
    def __init__(self) -> None:
        pass

    def get_project(self, id: str, session) -> Optional[ProjectModel]:
        pass

    def update_project(self, id: str, project_entity: ProjectEntity, session) -> Optional[ProjectModel]:
        pass

    def create_project(self, project_entity: ProjectEntity, session) -> Optional[ProjectModel]:
        pass

    def remove_project(self, id: str, session) -> bool:  # type: ignore
        pass
