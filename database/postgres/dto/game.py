from pydantic import BaseModel, Field
from typing import Optional

class GameDTO(BaseModel):
    game_id: Optional[int] = Field(None)
    league_id: Optional[int] = Field(None)
    sport_id: int = Field(...)
    country_id: Optional[int] = Field(None)
    team_away_id: Optional[int] = Field(None)
    team_home_id: Optional[int] = Field(None)
    score_away_team: Optional[int] = Field(None)
    score_home_team: Optional[int] = Field(None)
    status: Optional[str] = Field(None)
    type: Optional[str] = Field(None)
    time: Optional[str] = Field(None)
    date: Optional[str] = Field(None)
    api_id: Optional[int] = Field(None)

    class Config:
        from_attributes = True
