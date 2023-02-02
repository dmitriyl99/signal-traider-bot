from pydantic import BaseModel
from typing import Optional


class PaymeForm(BaseModel):
    method: str
    params: dict
    id: int


class CloudPaymentsPost3dSecureForm(BaseModel):
    MD: str
    PaRes: str


class CloudPaymentsForm(BaseModel):
    user_id: int
    subscription_id: int
    payment_id: int
    subscription_condition_id: int
