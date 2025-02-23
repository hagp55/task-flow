from datetime import datetime

from src.apps.tasks.enums import Priority, Status
from src.core import schemas


class TaskIn(schemas.InputApiSchema):
    name: str
    project_id: int | None = None
    priority: Priority | None = Priority.low
    status: Status | None = Status.pending


class TaskOut(schemas.OutputApiSchema):
    id: int
    name: str
    project_id: int
    priority: Priority | None = Priority.low
    status: Status | None = Status.pending
    created_at: datetime
    updated_at: datetime
