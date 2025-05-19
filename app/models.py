from typing import List
from sqlalchemy import String, Column, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


todo_item_recipient = Table(
    "todo_item_recipient",
    Base.metadata,
    Column("todo_item", ForeignKey("todo_item.id"), primary_key=True),
    Column("recipient_id", ForeignKey("recipient.id"), primary_key=True),
)


class TodoItem(Base):
    __tablename__ = "todo_item"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str]
    watchers: Mapped[List["Recipient"]] = relationship(
        secondary=todo_item_recipient, back_populates="watching"
    )

    def __repr__(self) -> str:
        return f"TodoItem(id={self.id!r}, title={self.title!r}, content={self.content!r}, watcher={self.watchers!r})"


class Recipient(Base):
    __tablename__ = "recipient"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    watching: Mapped[List["TodoItem"]] = relationship(
        secondary=todo_item_recipient, back_populates="watchers"
    )
