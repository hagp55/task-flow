from pydantic import Field

from src.core.schemas import OutputApiSchema


class GoogleUserDataOut(OutputApiSchema):
    id: int | None = None
    email: str
    name: str


class YandexUserDataOut(OutputApiSchema):
    id: int | None = None
    login: str
    email: str = Field(alias="default_email")
    name: str = Field(alias="real_name")
