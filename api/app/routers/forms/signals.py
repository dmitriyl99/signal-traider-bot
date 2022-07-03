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
    price: int
    tr_1: str
    tr_2: str
    sl: str
