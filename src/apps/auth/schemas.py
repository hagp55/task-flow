from src.core.schemas import OutputApiSchema


class GoogleUserDataOut(OutputApiSchema):
    id: int | None = None
    email: str
    name: str
    google_access_token: str
