from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class TeamsLeagueDTO(BaseModel):
    sport_id: Optional[int] = None
    league_id: Optional[int] = None
    country_id: Optional[int] = None
    page: Optional[int] = 0
    per_page: Optional[int] = 9

    def to_dict(self):
        filters = {}
        if self.sport_id is not None:
            filters["teams.sport_id"] = self.sport_id
        if self.league_id is not None:
            filters["leagues.api_id"] = self.league_id
        if self.country_id is not None:
            filters["countries.api_id"] = self.country_id
        return filters

    def get_pagination(self):
        if self.page != 0:
            offset = (self.page - 1) * self.per_page
            limit = self.per_page
            return offset, limit
        else:
            return None, None

class BaseDTO(BaseModel):
    pass

class TeamsStatisticsOrPlayersDTO(BaseDTO):
    sport_id: Optional[str] = None
    team_id: Optional[int] = None
    league_id: Optional[int] = None


class SearchDTO(BaseModel):
    sport_id: Optional[int] = None
    country_id: Optional[int] = None
    letter: Optional[str] = None
    page: Optional[int] = 0
    per_page: Optional[int] = 9

    def to_dict(self):
        filters = {}
        if self.sport_id is not None:
            filters["leagues.sport_id"] = self.sport_id
        if self.country_id is not None:
            filters["countries.api_id"] = self.country_id
        return filters

    def get_pagination(self):
        if self.page != 0:
            offset = (self.page - 1) * self.per_page
            limit = self.per_page
            return offset, limit
        else:
            return None, None

    @field_validator("letter", mode="before")
    def clean_letter(cls, value: Optional[str]) -> Optional[str]:
        if value and isinstance(value, str):
            return ' '.join(value.split()).lower()
        return None

    @field_validator("country_id", mode="before")
    def check_num(cls, value: Optional[int]) -> Optional[int]:
        if value == 0:
            return None
        return value


class SportsLeagueDTO(BaseModel):
    sport_id: Optional[int] = None
    page: Optional[int] = 0
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


class GamesDTO(BaseModel):
    sport_id: Optional[int] = None
    league_id: Optional[int] = None
    country_id: Optional[int] = None
    status: Optional[str] = None
    date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
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
            filters["games.date"] = self.date
        return filters

    def get_pagination(self):
        if self.page != 0:
            offset = (self.page - 1) * self.per_page
            limit = self.per_page
            return offset, limit
        else:
            return None, None


