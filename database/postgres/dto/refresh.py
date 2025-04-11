from pydantic import BaseModel, Field
from typing import Optional
import datetime

class RefreshTokenDTO(BaseModel):
    id: Optional[int] = Field(default=None)
    user_id: int = Field(...)
    last_ip: str = Field(...)
    last_device: str = Field(...)
    nonce: str = Field(...)