from datetime import datetime

from pydantic import AliasGenerator, BaseModel, ConfigDict, field_serializer
from pydantic.alias_generators import to_camel


class InputApiSchema(BaseModel):
    model_config = ConfigDict(
        str_strip_whitespace=True,
        use_enum_values=True,
        populate_by_name=True,
        alias_generator=AliasGenerator(
            validation_alias=to_camel,
        ),
    )


class OutputApiSchema(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=AliasGenerator(
            serialization_alias=to_camel,
            validation_alias=to_camel,
        ),
    )

    @field_serializer("created_at", "updated_at", "date_joined", "last_login", check_fields=False)
    def serialize_datetime(self, value: datetime) -> str:
        return value.strftime("%Y-%m-%d %H:%M:%S")
