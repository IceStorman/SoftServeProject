from pydantic import BaseModel, Field
from typing import Optional
from typing import Dict

class TeamDTO(BaseModel):
    team_index_id: Optional[int] = Field(None)
    sport_id: int = Field(...)
    name: str = Field(...)
    logo: Optional[str] = Field(None)
    api_id: Optional[int] = Field(None)
    league_id: Optional[int] = Field(None)

    class Config:
        from_attributes = True
