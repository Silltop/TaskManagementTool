import uuid
from datetime import datetime, timezone
from typing import Annotated, Optional, Union

from fastapi import Depends
from sqlmodel import Session, select

from adapters.db_connector import get_session
from domains.entities import ProjectEntity
from domains.models import ProjectModel
from ports.project_port import ProjectPort

SessionDep = Annotated[Session, Depends(get_session)]


class Project(ProjectPort):
    def get_project(self, id: str, session: SessionDep) -> ProjectModel | None:
        project = session.exec(select(ProjectModel)).all()
        for proj in project:
            if proj.id == uuid.UUID(str(id)):
                return proj
        return None

    def create_project(self, project_entity: ProjectEntity, session: Session) -> Union[ProjectModel, None]:
        existing_project = session.exec(select(ProjectModel).where(ProjectModel.id == project_entity.id)).first()
        if existing_project:
            return None
        new_project = ProjectModel(**project_entity.__dict__)
        session.add(new_project)
        session.commit()
        session.refresh(new_project)
        return new_project

    def update_project(self, id: str, project_entity: ProjectEntity, session: Session) -> Optional[ProjectModel]:
        existing_project = session.exec(select(ProjectModel).where(ProjectModel.id == uuid.UUID(str(id)))).first()
        if not existing_project:
            return None
        for key, value in project_entity.__dict__.items():
            if value is not None:
                setattr(existing_project, key, value)
        existing_project.updated_at = datetime.now(timezone.utc)
        session.add(existing_project)
        session.commit()
        session.refresh(existing_project)
        return existing_project

    def remove_project(self, id: str, session: Session) -> bool:
        existing_project = session.exec(select(ProjectModel).where(ProjectModel.id == uuid.UUID(str(id)))).first()
        if not existing_project:
            return False
        session.delete(existing_project)
        session.commit()
        return True
