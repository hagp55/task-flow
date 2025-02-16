from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base


class Task(Base):
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
        ),
    )

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, name={self.name!r})"


class Category(Base):
    id: Mapped[int] = mapped_column(
        primary_key=True,
    )
    name: Mapped[str]

    def __repr__(self) -> str:
        return f"Category(id={self.id!r}, name={self.name!r})"
