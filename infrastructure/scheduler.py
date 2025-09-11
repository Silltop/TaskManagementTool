from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from application.notifications import deadline_watcher


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(deadline_watcher, "interval", minutes=60)
    scheduler.start()
    yield
