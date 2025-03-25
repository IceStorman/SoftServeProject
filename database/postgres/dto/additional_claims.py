from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import datetime

class AdditionalClaimsDTO(BaseModel):
    user_id: int = Field(...)
    email: str = Field(...)
    username: str = Field(...)
    new_user: bool = Field(...)
    nonce: str = Field(default=None)

    class Config:  
        model_config = ConfigDict(from_attributes=True)