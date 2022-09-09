from typing import Optional

from pydantic import BaseModel
from enum import Enum


class ExecutionMethodEnum(str, Enum):
    sell = 'sell'
    buy = 'buy'
    sell_limit = 'sell_limit'
    buy_limit = 'buy_limit'
    sell_stop = 'sell_stop'
    buy_stop = 'buy_stop'


class CreateSignalForm(BaseModel):
    currency_pair: str
    execution_method: ExecutionMethodEnum
    price: float
    tr_1: Optional[str] = None
    tr_2: Optional[str] = None
    sl: Optional[str] = None


class SignalMessageForm(BaseModel):
    text: str
