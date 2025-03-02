import uuid
from datetime import datetime

from pydantic import Field

from src.apps.tasks.schemas import TaskOut
from src.core.schemas import InputApiSchema, OutputApiSchema


class ProjectIn(InputApiSchema):
    name: str = Field(min_length=2, max_length=250, examples=["TaskMania"])


class ProjectOut(OutputApiSchema):
    id: uuid.UUID
    name: str = Field(min_length=2, max_length=250, examples=["TaskMania"])
    created_at: datetime
    updated_at: datetime
    tasks: list[TaskOut] | None = None
