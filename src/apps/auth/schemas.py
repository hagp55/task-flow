from pydantic import Field

from src.core.schemas import OutputApiSchema


class GoogleUserDataOut(OutputApiSchema):
    id: int | None = None
    email: str
    name: str
    google_access_token: str


class YandexUserDataOut(OutputApiSchema):
    id: int | None = None
    login: str
    email: str = Field(alias="default_email")
    name: str = Field(alias="real_name")
    access_token: str
