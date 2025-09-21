from fastapi import FastAPI

from routers.task import task_router
from db.database import create_tables

create_tables()
app = FastAPI()
app.include_router(task_router)