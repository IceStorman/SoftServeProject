from pydantic import BaseModel
from typing import Optional


class GameOutputDTO(BaseModel):
    id: int
    status: str
    date: str
    time: Optional[str]
    league_name: str
    league_logo: str
    country_name: str
    home_team_name: str
    home_team_logo: str
    away_team_name: str
    away_team_logo: str
    home_score: Optional[int] = None
    away_score: Optional[int] = None

    def to_dict(self):
        return dict(self)


class TeamsLeagueOutputDTO(BaseModel):
    league_name:  Optional[str]
    country_name:  Optional[str]
    team_name: str
    logo: str
    id: str

    def to_dict(self):
        return dict(self)


class SportsOutputDTO(BaseModel):
    id: int
    sport: str
    logo: str

    def to_dict(self):
        return dict(self)


class SportsLeagueOutputDTO(BaseModel):
    id: int
    sport: Optional[int]
    logo: str
    name: str
    count: int

    def to_dict(self):
        return dict(self)


class CountriesOutputDTO(BaseModel):
    id: Optional[int]
    flag: Optional[str]
    name: str

    def to_dict(self):
        return dict(self)
