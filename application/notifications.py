from sqlmodel import Session

from adapters.db_connector import engine
from application.tasks import Task, logger


def deadline_watcher():
    with Session(engine) as session:
        tasks = Task().check_deadlines(session=session, due=24)
        if tasks:
            logger.info(f"Upcoming deadlines for tasks: {[task.id for task in tasks]}")
