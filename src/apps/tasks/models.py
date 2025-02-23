from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base, str_500
from src.core.models import TimestampMixin


class Task(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_500]
    priority: Mapped[str]
    status: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )
    project_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "projects.id",
            ondelete="CASCADE",
        )
    )

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, name={self.name!r})"
