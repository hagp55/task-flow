from pydantic import Field

from src.core.schemas import InputApiSchema, OutputApiSchema


class ProjectIn(InputApiSchema):
    name: str = Field(min_length=2, max_length=250, examples=["big cool project"])


class ProjectOut(OutputApiSchema):
    id: int
    name: str = Field(min_length=2, max_length=250, examples=["big cool project"])
