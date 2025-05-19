from typing import Annotated

from fastapi import APIRouter, Depends,  HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.schemas import TodoItem, TodoItemCreate, TodoItemPartialUpdate
from app.models import TodoItem as TodoItemBase, Recipient as RecipientBase

router = APIRouter(prefix="/todos")

SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


@router.post("/", response_model=TodoItem)
async def create_todo(todo: TodoItemCreate, session: SessionDep):
    new_todo = TodoItemBase(**todo.model_dump(exclude={'watchers'}))

    if todo.watchers and len(todo.watchers):
        result = await session.execute(
            select(RecipientBase)
            .where(RecipientBase.email.in_(todo.watchers))
        )
        existing = result.scalars().all()
        existing_emails = {r.email for r in existing}
        missing_emails = set(todo.watchers) - existing_emails

        new_recipients = [RecipientBase(email=e) for e in missing_emails]
        session.add_all(new_recipients)
        new_todo.watchers = [*existing, *new_recipients]

    session.add(new_todo)
    await session.commit()
    await session.refresh(new_todo, attribute_names=['title', 'content', 'watchers'])
    return new_todo


@router.get("/", response_model=list[TodoItem])
async def read_todos(
    session: SessionDep,
):
    todos = (await session.execute(
        select(TodoItemBase)
        .options(selectinload(TodoItemBase.watchers)))
    ).scalars().all()
    return todos


@router.patch("/{todo_id}", response_model=TodoItem)
async def update_todo(
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
    if todo_update.title is not None:
        todo.title = todo_update.title

    if todo_update.content is not None:
        todo.content = todo_update.content

    if todo_update.watcher is not None:
        recipient = (await session.execute(
            select(RecipientBase)
            .where(RecipientBase.email == todo_update.watcher)
        )
        ).scalar_one_or_none() or RecipientBase(email=todo_update.watcher)
        if recipient not in todo.watchers:
            todo.watchers.append(recipient)
    await session.commit()
    await session.refresh(todo, attribute_names=['title', 'content', 'watchers'])
    return todo


@router.get("/{todo_id}", response_model=TodoItem)
async def read_todo(todo_id: int, session: SessionDep):
    todo = (await session.execute(
        select(TodoItemBase)
        .where(TodoItemBase.id == todo_id)
        .options(selectinload(TodoItemBase.watchers)))
    ).scalar()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo
