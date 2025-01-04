from pydantic import BaseModel, Field
from typing import Optional

class LeagueDTO(BaseModel):
    league_id: Optional[int] = Field(None)
    api_id: Optional[int] = Field(None)
    name: str = Field(...)
    logo: Optional[str] = Field(None)
    sport_id: int = Field(...)
    country: Optional[int] = Field(None)

    class Config:
        from_attributes = True
