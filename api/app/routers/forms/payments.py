from pydantic import BaseModel
from typing import Optional


class PaymeForm(BaseModel):
    method: str
    params: dict
    id: int
