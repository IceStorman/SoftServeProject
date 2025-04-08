from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class InteractionWithNewsDTO(BaseModel):
    interaction_id : Optional[int] = Field(None)
    news_id : int = Field(...)
    user_id : int = Field(...)
    interaction_type: int = Field(...)
    timestamp: Optional[datetime] = Field(None)

    class Config:
        from_attributes = True