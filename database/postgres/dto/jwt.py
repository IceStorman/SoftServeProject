from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import datetime

class JwtDTO(BaseModel):
    id: Optional[int] = Field(default=None)
    user_id: int = Field(...)
    jti: str = Field(...)
    token_type: str = Field(...)
    token: str = Field(...)
    revoked: bool = Field(...)
    expires_at: datetime.datetime = Field(...)
    updated_at: Optional[datetime.datetime] = Field(default_factory=datetime.datetime.utcnow)

    class Config:  
        model_config = ConfigDict(from_attributes=True) 