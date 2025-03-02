import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.apps.tasks.enums import Priority, Status
from src.core.db import Base, str_500
from src.core.models import TimestampMixin

if TYPE_CHECKING:
    from src.apps.projects.models import Project


class Task(TimestampMixin, Base):
    name: Mapped[str_500]
    priority: Mapped[Priority] = mapped_column(
        default=Priority.low,
        server_default=text("'low'"),
    )
    status: Mapped[Status] = mapped_column(
        default=Status.pending,
        server_default=text("'pending'"),
    )
    deadline: Mapped[datetime | None]
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        )
    )
    project_id: Mapped[uuid.UUID | None] = mapped_column(
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
