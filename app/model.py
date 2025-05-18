from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class TodoItem(Base):
    __tablename__ = "todo_item"

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str]

    def __repr__(self) -> str:
        return f"TodoItem(id={self.id!r}, title={self.title!r}, description={self.description!r})"
