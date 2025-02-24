from datetime import datetime

from pydantic import Field

from src.apps.tasks.enums import Priority, Status
from src.core import schemas


class TaskIn(schemas.InputApiSchema):
    name: str = Field(
        min_length=2,
        max_length=500,
        examples=["Spend 10 minutes meditating to clear the mind."],
    )
    project_id: int | None = Field(default=None, ge=1, examples=[None])
    priority: Priority | None = Field(
        default=Priority.low,
        examples=["low", "medium", "high"],
    )

    status: Status | None = Field(
        default=Status.pending,
        examples=["pending", "progress", "completed"],
    )


class TaskOut(schemas.OutputApiSchema):
    id: int
    name: str
    project_id: int | None
    priority: Priority | None = Priority.low
    status: Status | None = Status.pending
    created_at: datetime
    updated_at: datetime
