from pydantic import BaseModel


class CreateUtmCommand(BaseModel):
    name: str
