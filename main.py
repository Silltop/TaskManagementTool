from fastapi import FastAPI
from sqlmodel import create_engine

from adapters.api import projects, tasks
from adapters.logging_conf.log_config import setup_logging

app = FastAPI()
setup_logging()
app.include_router(projects.router)
app.include_router(tasks.router)

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# https://fastapi.tiangolo.com/tutorial/background-tasks/#create-a-task-function
