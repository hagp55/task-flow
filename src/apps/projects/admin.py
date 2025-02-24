from typing import Any

from sqladmin import ModelView

from src.apps.auth.services import AuthService
from src.apps.projects.models import Project


class ProjectAdmin(ModelView, model=Project):
    column_list = (
        Project.id,
        Project.name,
    )
    column_searchable_list = [
        Project.name,
    ]
    column_sortable_list = [
        Project.name,
    ]
    form_create_rules = [
        "name",
    ]
    form_edit_rules = [
        "name",
    ]
    name = "Project"
    name_plural = "Projects"
    icon = "fa-solid fa-diagram-project"
    page_size = 25

    async def on_model_change(self, data, model, is_created, request) -> None:
        if is_created:
            token: Any | None = request.session.get("token")
            if token:
                user_id: int = AuthService.get_user_id_from_access_token(
                    access_token=token,
                )
                data["user_id"] = user_id
