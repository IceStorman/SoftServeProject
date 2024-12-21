from pydantic import BaseModel, Field
from typing import Optional, Union
from datetime import datetime


class TeamsLeagueDTO(BaseModel):
    sport: Optional[Union[int, str]] = None
    league_id: Optional[int] = None
    country_id: Optional[int] = None
    page: Optional[int] = 1
    per_page: Optional[int] = 9

class TeamsStatisticsOrPlayersDTO(BaseModel):
    sport: Optional[Union[int, str]] = None
    team_id: Optional[int] = None
    league_id: Optional[int] = None

class SportsLeagueDTO(BaseModel):
    sport_id: Optional[Union[int, str]] = None
    page: Optional[int] = 1
    per_page: Optional[int] = 9

    def to_dict(self):
        filters = {}
        if self.sport_id is not None:
            filters["leagues.sport_id"] = self.sport_id
        return filters

    def get_pagination(self):
        if self.page != 0:
            offset = (self.page - 1) * self.per_page
            limit = self.per_page
            return offset, limit
        else:
            return None, None

# class GamesDTO(BaseModel):
#     sport_id: Optional[Union[int, str]] = None
#     league_id: Optional[int] = None
#     country_id: Optional[int] = None
#     status: Optional[str] = None
#     date: Optional[str] = datetime.now().date()
#     page: Optional[int] = 1
#     per_page: Optional[int] = 9
#
#     def to_dict(self):
#         return dict(self)
class GamesDTO(BaseModel):
    sport_id: Optional[Union[int, str]] = None
    league_id: Optional[int] = None
    country_id: Optional[int] = None
    status: Optional[str] = None
    date: Optional[str] = None
    page: Optional[int] = 0
    per_page: Optional[int] = 9

    def to_dict(self):
        filters = {}
        if self.sport_id is not None:
            filters["games.sport_id"] = self.sport_id
        if self.league_id is not None:
            filters["games.league_id"] = self.league_id
        if self.country_id is not None:
            filters["games.country_id"] = self.country_id
        if self.date is not None:
            filters["games.date"] = self.date.strftime('%Y-%m-%d')
        return filters

    def get_pagination(self):
        if self.page != 0:
            offset = (self.page - 1) * self.per_page
            limit = self.per_page
            return offset, limit
        else:
            return None, None



class GameOutputDTO(BaseModel):
    game_id: int
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
    league_name: str
    country_name: str
    team_name: str

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

    def to_dict(self):
        return dict(self)
