"""Add table User

Revision ID: 0f64a05f329c
Revises:
Create Date: 2025-03-02 08:24:51.400617

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0f64a05f329c"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("email", sa.String(length=250), nullable=False),
        sa.Column("password", sa.String(length=250), nullable=True),
        sa.Column("first_name", sa.String(length=250), nullable=True),
        sa.Column("last_name", sa.String(length=250), nullable=True),
        sa.Column("date_joined", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("last_login", sa.DateTime(), server_default=sa.text("now()"), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_staff", sa.Boolean(), nullable=False),
        sa.Column("is_super_user", sa.Boolean(), nullable=False),
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("users_pkey")),
        sa.UniqueConstraint("email", name=op.f("users_email_key")),
    )


def downgrade() -> None:
    op.drop_table("users")
