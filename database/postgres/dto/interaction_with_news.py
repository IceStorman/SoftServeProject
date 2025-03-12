from pydantic import BaseModel, Field
from typing import Optional

class InteractionWithNewsDTO(BaseModel):
    interaction_id : int = Field(...)
    news_id : int = Field(...)
    user_id : int = Field(...)
    type_of_interaction: int = Field(...)
    timestamp: Optional[int] = Field(None)
