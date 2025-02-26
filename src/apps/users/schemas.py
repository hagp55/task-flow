from datetime import datetime

from pydantic import EmailStr, Field

from src.core.schemas import InputApiSchema, OutputApiSchema


class UserLoginIn(InputApiSchema):
    email: str = Field(min_length=6, max_length=250, examples=["beazley@example.com"])
    password: str = Field(min_length=6, max_length=250, examples=["Str0ngP@ssw0rd!"])


class UserLoginOut(OutputApiSchema):
    id: int
    access_token: str


class UserSignUpIn(InputApiSchema):
    email: EmailStr = Field(min_length=6, max_length=250, examples=["beazley@example.com"])
    password: str = Field(min_length=6, max_length=250, examples=["Str0ngP@ssw0rd!"])
    first_name: str | None = Field(min_length=2, max_length=250, examples=[None])
    last_name: str | None = Field(min_length=2, max_length=255, examples=[None])


class ChangeUserPasswordIn(InputApiSchema):
    email: EmailStr = Field(min_length=6, max_length=250, examples=["beazley@example.com"])
    old_password: str = Field(min_length=6, max_length=250, examples=["Str0ngP@ssw0rd!"])
    new_password: str = Field(min_length=6, max_length=250, examples=["NewStr0ngP@ssw0rd!"])


class UserMeOut(OutputApiSchema):
    first_name: str | None = Field(min_length=2, max_length=250, examples=["David"])
    last_name: str | None = Field(min_length=2, max_length=255, examples=["Beazley"])
    email: EmailStr = Field(min_length=6, max_length=250, examples=["beazley@example.com"])
    is_active: bool | None
    is_staff: bool | None
    is_super_user: bool | None
    date_joined: datetime | None
    last_login: datetime | None
