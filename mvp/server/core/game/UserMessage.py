from typing import Literal

from pydantic import BaseModel


class UserMessage(BaseModel):
    type: Literal["WARNING", "INFO"]
    content: str
    seen: bool = False
