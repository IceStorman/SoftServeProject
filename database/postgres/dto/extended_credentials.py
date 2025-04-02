from pydantic import BaseModel, Field
from typing import Optional
import datetime

class ExtendedCredantialsDTO(BaseModel):
    user_id: int = Field(...)
    email: str = Field(...)
    username: str = Field(...)
    new_user: bool = Field(...)