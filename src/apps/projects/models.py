import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.db import Base, str_250
from src.core.models import TimestampMixin

if TYPE_CHECKING:
    from src.apps.tasks.models import Task


class Project(TimestampMixin, Base):
    # id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_250]
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )
    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project",
        lazy="selectin",
    )
    __table_args__ = (
        UniqueConstraint(
            "name",
            "user_id",
        ),
    )

    def __repr__(self) -> str:
        return f"Project(id={self.id!r}, name={self.name!r})"
