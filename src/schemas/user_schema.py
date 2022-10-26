from pydantic import BaseModel
from pydantic.fields import Field


class User(BaseModel):
    id: int
    username: str
    password: str = Field(None, exclude=True)
