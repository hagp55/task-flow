from pydantic import EmailStr, Field

from src.core.schemas import OutputApiSchema


class GoogleUserDataOut(OutputApiSchema):
    id: int | None = None
    email: EmailStr
    name: str


class YandexUserDataOut(OutputApiSchema):
    id: int | None = None
    login: str
    email: EmailStr = Field(alias="default_email")
    name: str = Field(alias="real_name")
