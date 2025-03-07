from pydantic import BaseModel, Field
from typing import Optional
from typing import Dict

class PlayerDTO(BaseModel):
    player_id: Optional[int] = Field(None)
    name: str = Field(...)
    logo: Optional[str] = Field(None)
    team_index_id: Optional[int] = Field(None)
    sport_id: int = Field(...)
    api_id: Optional[int] = Field(None)

    class Config:
        from_attributes = True
