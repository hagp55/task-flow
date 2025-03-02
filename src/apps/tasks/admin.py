import uuid
from typing import Any

from sqladmin import ModelView

from src.apps.auth.services import AuthService
from src.apps.tasks.models import Task


class TaskAdmin(ModelView, model=Task):
    column_list = (
        Task.id,
        Task.name,
    )
    column_searchable_list = [
        Task.name,
    ]
    column_sortable_list = [
        Task.name,
    ]

    name = "Task"
    name_plural = "Tasks"
    icon = "fa-solid fa-list-check"
    page_size = 25

    async def on_model_change(self, data, model, is_created, request) -> None:
        if is_created:
            token: Any | None = request.session.get("token")
            if token:
                user_id: uuid.UUID = AuthService.get_user_id_from_access_token(
                    access_token=token,
                )
                data["user_id"] = user_id
