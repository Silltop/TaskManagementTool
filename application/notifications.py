from sqlmodel import Session

from adapters.db_connector import engine
from application.tasks import TaskService, logger


def deadline_watcher():
    with Session(engine) as session:
        tasks = TaskService().check_deadlines(session=session, due=1)
        if tasks:
            logger.info(f"Upcoming deadlines for tasks: {[task.id for task in tasks]}")
