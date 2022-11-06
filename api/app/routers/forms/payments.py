from pydantic import BaseModel
from typing import Optional


class ClickForm(BaseModel):
    merchant_trans_id: Optional[str] = None
    click_trans_id: Optional[str] = None
    service_id: Optional[int] = None
    click_paydoc_id: Optional[int] = None
    amount: Optional[int] = None
    action: Optional[str] = None
    error: Optional[str] = None
    error_note: Optional[str] = None
    sign_time: Optional[str] = None
    sign_string: Optional[str] = None
    merchant_prepare_id: Optional[int] = None
