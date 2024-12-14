from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

class UniversalResponseDTO(BaseModel):
    sport: Optional[Union[int, str]] = None
    team_id: Optional[int] = None
    league_id: Optional[int] = None
    country_id: Optional[int] = None

class TeamsLeagueDTO(BaseModel):
    sport: Optional[Union[int, str]] = None
    league_id: Optional[int] = None
    country_id: Optional[int] = None

class TeamsStatisticsOrPlayersDTO(BaseModel):
    sport: Optional[Union[int, str]] = None
    team_id: Optional[int] = None

class SportsLeagueDTO(BaseModel):
    sport: Optional[Union[int, str]] = None
    page: Optional[int] = 1
    per_page: Optional[int] = 9

class GamesDTO(BaseModel):
    sport_id: Optional[Union[int, str]] = None
    league_id: Optional[int] = None
    country_id: Optional[int] = None
    status: Optional[str] = None
    date: Optional[str] = datetime.now().date()






class GameOutputDTO(BaseModel):
    game_id: int
    status: str
    date: str
    time: str
    league_name: str
    country_name: str
    home_team_name: str
    home_team_logo: str
    away_team_name: str
    away_team_logo: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None

class TeamsLeagueOutputDTO(BaseModel):
    league_name: str
    country_name: str
    team_name: str

class SportsOutputDTO(BaseModel):
    id: int
    sport: str
    logo: str

class SportsLeagueOutputDTO(BaseModel):
    id: int
    sport: str
    logo: str
    name: str

