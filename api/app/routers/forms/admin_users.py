from pydantic import BaseModel
from typing import List


class CreateAdminUserForm(BaseModel):
    username: str
    password: str
    password_confirmation: str
    roles: List[int] | None = None


class ChangePasswordForm(BaseModel):
    password: str
    password_confirmation: str
