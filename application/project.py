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


class ProjectService(ProjectPort):
    def get_project(self, id: uuid.UUID, session: SessionDep) -> ProjectModel | None:
        project = session.exec(select(ProjectModel)).all()
        for proj in project:
            if proj.id == id:
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

    def update_project(self, id: uuid.UUID, project_entity: ProjectEntity, session: Session) -> Optional[ProjectModel]:
        existing_project = session.exec(select(ProjectModel).where(ProjectModel.id == id)).first()
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

    def remove_project(self, id: uuid.UUID, session: Session) -> bool:
        existing_project = session.exec(select(ProjectModel).where(ProjectModel.id == id)).first()
        if not existing_project:
            return False
        session.delete(existing_project)
        session.commit()
        return True

    def get_project_completed_status(self, id: uuid.UUID, session: Session) -> bool:
        project = session.exec(select(ProjectModel).where(ProjectModel.id == id)).first()
        if not project:
            return False
        return project.completed

    def set_project_completed_status(self, id: uuid.UUID, status: bool, session: Session) -> Optional[ProjectModel]:
        project = session.exec(select(ProjectModel).where(ProjectModel.id == id)).first()
        if not project:
            return None
        project.completed = status
        project.updated_at = datetime.now(timezone.utc)
        session.add(project)
        session.commit()
        session.refresh(project)
        return project
