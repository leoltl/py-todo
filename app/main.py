from fastapi import FastAPI

from app.routers.todo import router as todo_router

app = FastAPI()

app.include_router(todo_router)
