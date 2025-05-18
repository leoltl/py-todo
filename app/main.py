from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.schemas import TodoItem, TodoItemCreate
from app.model import TodoItem as TodoItemBase


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

app = FastAPI()


@app.post("/todos/", response_model=TodoItem)
async def create_todo(todo: TodoItemCreate, session: SessionDep):
    new_todo = TodoItemBase(**todo.model_dump())
    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo)
    return new_todo


@app.get("/todos/", response_model=Sequence[TodoItem])
async def read_todos(
    session: SessionDep,
):
    todos = (await session.execute(select(TodoItemBase))).scalars().all()
    return todos


@app.get("/todos/{todo_id}", response_model=TodoItem)
async def read_todo(todo_id: int, session: SessionDep):
    todo = (await session.execute(select(TodoItemBase).where(TodoItemBase.id == todo_id))).scalar()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
