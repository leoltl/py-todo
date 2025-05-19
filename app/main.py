from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers.todo import router as todo_router
from app.database import Listener as PgListener


@asynccontextmanager
async def lifespan(app: FastAPI):
    PgListener().init()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(todo_router)
