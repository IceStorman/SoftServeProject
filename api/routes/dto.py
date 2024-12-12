from pydantic import BaseModel
from typing import Optional, Union

class UniversalResponseDTO(BaseModel):
    sport: Optional[Union[int, str]] = None
    team_id: Optional[int] = None
    league_id: Optional[int] = None
    country_id: Optional[int] = None