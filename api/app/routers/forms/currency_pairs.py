from pydantic import BaseModel


class SaveCurrencyPairForm(BaseModel):
    pair_name: str
