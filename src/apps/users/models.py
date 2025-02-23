from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.core.db import Base, boolean_false, boolean_true, str_250_or_none, uniq_str_250_or_none


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[uniq_str_250_or_none]
    password: Mapped[str_250_or_none]
    email: Mapped[uniq_str_250_or_none]
    first_name: Mapped[str_250_or_none]
    last_name: Mapped[str_250_or_none]
    date_joined: Mapped[datetime | None] = mapped_column(server_default=func.now())
    last_login: Mapped[datetime | None] = mapped_column(server_onupdate=func.now())
    is_active: Mapped[boolean_true]
    is_staff: Mapped[boolean_false]
    is_super_user: Mapped[boolean_false]

    def __repr__(self) -> str:
        return f"User (id:{self.id!r}, email: {self.email!r})"

    @property
    def get_full_name(self) -> str:
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name: str = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    @property
    def get_short_name(self) -> str | None:
        """Return the short name for the user."""
        return self.first_name
