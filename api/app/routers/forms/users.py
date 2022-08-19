from pydantic import BaseModel


class CreateUserForm(BaseModel):
    name: str
    phone: str
    subscription_id: int
    subscription_condition_id: int
