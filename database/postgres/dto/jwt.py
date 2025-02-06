from pydantic import BaseModel, Field
from typing import Optional
import datetime

class jwtDTO(BaseModel):
    id: Optional[int] = Field(default=None)
    user_id: int = Field(...)
    jti: str = Field(...)
    token_type: str = Field(...)
    revoked: bool = Field(...)
    expires_at: datetime.datetime = Field(...)
    created_at: Optional[datetime.datetime] = None
    updated_at: Optional[datetime.datetime] = None

    class Config:
        from_attributes = True
