from pydantic import BaseModel


class CreateAdminUserForm(BaseModel):
    username: str
    password: str
    password_confirmation: str


class ChangePasswordForm(BaseModel):
    password: str
    password_confirmation: str
