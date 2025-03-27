from pydantic import BaseModel, Field
from typing import Optional
import datetime

class ResponseDataDTO(BaseModel):
    user_id: int = Field(...)
    email: str = Field(...)
    username: str = Field(...)
    new_user: bool = Field(...)
    access_token: str = Field(...)
    refresh_token: str = Field(...)
    message: str = Field(...)

    class Config: 
        from_attributes = True