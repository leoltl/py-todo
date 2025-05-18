from typing import Optional
from pydantic import BaseModel, ConfigDict


class TodoItemCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str


class TodoItem(TodoItemCreate):
    id: int
