"""Add table Task

Revision ID: 6a973fbbe369
Revises: ddbb29277c49
Create Date: 2025-03-02 08:27:00.417073

"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "6a973fbbe369"
down_revision: str | None = "ddbb29277c49"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "tasks",
        sa.Column("name", sa.String(length=500), nullable=False),
        sa.Column(
            "priority",
            sa.Enum("low", "medium", "high", name="priority", create_type=False),
            server_default=sa.text("'low'"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum("pending", "progress", "completed", "expired", name="status", create_type=False),
            server_default=sa.text("'pending'"),
            nullable=False,
        ),
        sa.Column("deadline", sa.DateTime(), nullable=True),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("project_id", sa.UUID(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.ForeignKeyConstraint(
            ["project_id"], ["projects.id"], name=op.f("tasks_project_id_fkey"), ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("tasks_user_id_fkey"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("tasks_pkey")),
        sa.UniqueConstraint("name", "user_id", name=op.f("tasks_name_key")),
    )


def downgrade() -> None:
    op.drop_table("tasks")
    op.execute("DROP TYPE IF EXISTS priority")
    op.execute("DROP TYPE IF EXISTS status")
