from typing import Optional

from pydantic import BaseModel


class ClickPreparePaymentForm(BaseModel):
    click_trans_id: Optional[int] = None
    service_id: Optional[int] = None
    click_paydoc_id: Optional[int] = None
    merchant_trans_id: Optional[str] = None
    amount: Optional[float] = None
    action: Optional[int] = None
    error: Optional[int] = None
    error_note: Optional[str] = None
    sign_time: Optional[str] = None
    sign_string: Optional[str] = None
    merchant_prepare_id: Optional[str] = None
