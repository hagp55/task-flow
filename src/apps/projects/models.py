from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base, str_250
from src.core.models import TimestampMixin


class Project(TimestampMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str_250]
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
    )

    def __repr__(self) -> str:
        return f"Project(id={self.id!r}, name={self.name!r})"
