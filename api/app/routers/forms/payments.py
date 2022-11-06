from pydantic import BaseModel
from typing import Optional


class ClickForm(BaseModel):
    merchant_trans_id: Optional[str]
    click_trans_id: Optional[str]
    service_id: Optional[int]
    click_paydoc_id: Optional[int]
    amount: Optional[int]
    action: Optional[str]
    error: Optional[str]
    error_note: Optional[str]
    sign_time: Optional[str]
    sign_string: Optional[str]
    merchant_prepare_id: Optional[int]
