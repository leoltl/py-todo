from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session

from app.schemas import TodoItem, TodoItemCreate, TodoItemPartialUpdate
from app.model import TodoItem as TodoItemBase, Recipient as RecipientBase


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]

app = FastAPI()


@app.post("/todos/", response_model=TodoItem)
async def create_todo(todo: TodoItemCreate, session: SessionDep):
    new_todo = TodoItemBase(**todo.model_dump())
    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo, attribute_names=['title', 'content', 'watchers'])
    return new_todo


@app.get("/todos/", response_model=Sequence[TodoItem])
async def read_todos(
    session: SessionDep,
):
    todos = (await session.execute(
        select(TodoItemBase)
        .options(selectinload(TodoItemBase.watchers)))
    ).scalars().all()
    return todos


@app.patch("/todos/{todo_id}", response_model=TodoItem)
async def set_watchers(
    todo_id: int,
    todo_update: TodoItemPartialUpdate,
    session: SessionDep,
):
    todo = (await session
            .execute(
                select(TodoItemBase)
                .where(TodoItemBase.id == todo_id)
                .options(selectinload(TodoItemBase.watchers)))
            ).scalar_one()
    if todo_update.watcher is not None:
        recipient = (await session
                     .execute(
                         select(RecipientBase)
                         .where(RecipientBase.email == todo_update.watcher)
                     )
                     ).scalar_one_or_none() or RecipientBase(email=todo_update.watcher)
        if recipient not in todo.watchers:
            todo.watchers.append(recipient)
    await session.commit()
    await session.refresh(todo, attribute_names=['title', 'content', 'watchers'])
    return todo


@app.get("/todos/{todo_id}", response_model=TodoItem)
async def read_todo(todo_id: int, session: SessionDep):
    todo = (await session.execute(
        select(TodoItemBase)
        .where(TodoItemBase.id == todo_id)
        .options(selectinload(TodoItemBase.watchers)))
    ).scalar()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
