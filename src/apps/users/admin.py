from sqladmin import ModelView

from src.apps.auth.security import bcrypt_context
from src.apps.users.models import User


class UserAdmin(ModelView, model=User):
    column_list = (
        User.id,
        User.email,
        User.is_staff,
        User.is_super_user,
    )
    column_searchable_list = [
        User.email,
    ]
    column_sortable_list = [
        User.email,
    ]
    form_create_rules = [
        "email",
        "password",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_super_user",
    ]
    form_edit_rules = [
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_super_user",
    ]
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"
    page_size = 25

    async def on_model_change(self, data, model, is_created, request):
        if is_created:
            hashed_password: str = bcrypt_context.hash(data["password"])
            data["password"] = hashed_password
