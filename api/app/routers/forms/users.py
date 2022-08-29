from typing import Optional

from pydantic import BaseModel


class CreateUserForm(BaseModel):
    name: str
    phone: str
    subscription_id: Optional[int] = None
    subscription_condition_id: Optional[int] = None
    subscription_duration_in_days: Optional[int] = None


class UpdateUserForm(BaseModel):
    name: str
    phone: str
    subscription_id: Optional[int] = None
    subscription_condition_id: Optional[int] = None
    subscription_duration_in_days: Optional[int] = None
