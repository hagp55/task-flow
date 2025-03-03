import uuid
from datetime import datetime
from typing import Self

from pydantic import EmailStr, Field, field_validator, model_validator

from src.core.schemas import InputApiSchema, OutputApiSchema
from src.core.utils.auth.password_validation import (
    CommonPasswordValidator,
    NumericPasswordValidator,
    UserAttributeSimilarityValidator,
)


class UserLoginIn(InputApiSchema):
    email: EmailStr = Field(min_length=6, max_length=250, examples=["beazley@example.com"])
    password: str = Field(min_length=6, max_length=250, examples=["Str0ngP@ssw0rd!"])


class UserLoginOut(OutputApiSchema):
    id: uuid.UUID
    access_token: str


class UserSignUpIn(InputApiSchema):
    email: EmailStr = Field(min_length=6, max_length=250, examples=["beazley@example.com"])
    password: str = Field(min_length=6, max_length=250, examples=["Str0ngP@ssw0rd!"])
    first_name: str | None = Field(default=None, min_length=2, max_length=250, examples=[None])
    last_name: str | None = Field(default=None, min_length=2, max_length=255, examples=[None])

    @field_validator("password", mode="before")
    def validate_password_common(cls, value) -> str:
        password_validator = CommonPasswordValidator()
        password_validator.validate(password=value)
        return value

    @field_validator("password", mode="before")
    def validate_password_numeric(cls, value) -> str:
        password_validator = NumericPasswordValidator()
        password_validator.validate(password=value)
        return value

    @model_validator(mode="after")
    def validate_password_similarity(self) -> Self:
        password_validator = UserAttributeSimilarityValidator()
        password_validator.validate(password=self.password, user=self)
        return self


class ChangeUserPasswordIn(InputApiSchema):
    email: EmailStr = Field(min_length=6, max_length=250, examples=["beazley@example.com"])
    old_password: str = Field(min_length=6, max_length=250, examples=["Str0ngP@ssw0rd!"])
    new_password: str = Field(min_length=6, max_length=250, examples=["NewStr0ngP@ssw0rd!"])

    @field_validator("new_password", mode="before")
    def validate_password_common(cls, value) -> str:
        password_validator = CommonPasswordValidator()
        password_validator.validate(password=value)
        return value

    @field_validator("new_password", mode="before")
    def validate_password_numeric(cls, value) -> str:
        password_validator = NumericPasswordValidator()
        password_validator.validate(password=value)
        return value

    @model_validator(mode="after")
    def validate_password_similarity(self) -> Self:
        password_validator = UserAttributeSimilarityValidator()
        password_validator.validate(password=self.new_password, user=self)
        return self


class UserMeOut(OutputApiSchema):
    id: uuid.UUID
    first_name: str | None = Field(min_length=2, max_length=250, examples=["David"])
    last_name: str | None = Field(min_length=2, max_length=255, examples=["Beazley"])
    email: EmailStr = Field(min_length=6, max_length=250, examples=["beazley@example.com"])
    is_active: bool | None
    is_staff: bool | None
    is_super_user: bool | None
    date_joined: datetime | None
    last_login: datetime | None
