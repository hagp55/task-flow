from src.core.schemas import InputApiSchema, OutputApiSchema


class UserLoginOut(OutputApiSchema):
    id: int
    access_token: str


class UserIn(InputApiSchema):
    username: str
    password: str
