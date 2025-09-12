import uvicorn
from fastapi import FastAPI
from sqlmodel import create_engine

from adapters.api import projects, tasks
from adapters.api.helpers import invalid_uuid_exception_handler
from adapters.db_connector import create_db_and_tables
from infrastructure.errors import ConversionUUIDError
from infrastructure.log_definition import logging_config
from infrastructure.scheduler import lifespan

app = FastAPI(lifespan=lifespan)

app.include_router(projects.router)
app.include_router(tasks.router)
app.add_exception_handler(ConversionUUIDError, invalid_uuid_exception_handler)  # type: ignore

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# https://fastapi.tiangolo.com/tutorial/background-tasks/#create-a-task-function

create_db_and_tables()

uvicorn.run(app, host="0.0.0.0", port=8000, log_config=logging_config, log_level="info")
