from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base, str_500
from src.core.models import TimestampMixin

if TYPE_CHECKING:
    from src.apps.projects.models import Project


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
    project: Mapped["Project"] = relationship(
        back_populates="tasks",
        lazy="joined",
    )

    __table_args__ = (
        UniqueConstraint(
            "name",
            "user_id",
        ),
    )

    def __repr__(self) -> str:
        return f"Task(id={self.id!r}, name={self.name!r})"
