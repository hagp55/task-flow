from src.core import schemas


class TaskIn(schemas.InputApiSchema):
    id: int
    name: str
    pomodoro_count: int
    category_id: int

    # @model_validator(mode="after")
    # def check_name_or_pomodoro_count_is_not_none(self) -> Self:
    #     if self.name is None and self.pomodoro_count is None:
    #         raise ValueError("Enter name or pomodoro_count")
    #     return self


class TaskOut(schemas.OutputApiSchema):
    id: int
    name: str
    pomodoro_count: int
    category_id: int
