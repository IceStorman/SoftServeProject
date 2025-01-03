from pydantic import BaseModel, Field
from typing import Optional

class SportDTO(BaseModel):
    sport_id: Optional[int] = Field(None)
    sport_name: str = Field(...)
    sport_img: Optional[str] = Field(None)

    class Config:
        from_attributes = True
