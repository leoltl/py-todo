from typing import List
from pydantic import BaseModel, ConfigDict


class Recipient(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    watching: List["TodoItem"]


class RecipientMinimal(BaseModel):
    id: int
    email: str


class TodoItemCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    content: str
    watchers: List[str] | None


class TodoItemPartialUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    watcher: str | None = None


class TodoItem(BaseModel):
    id: int
    title: str
    content: str
    watchers: List["RecipientMinimal"]
