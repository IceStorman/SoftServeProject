from sqlalchemy.orm import Query
from database.models import Games
from service.api_logic.scripts import get_sport_by_name
from service.api_logic.filter_manager.base_filter_manager import BaseFilterManager
from service.api_logic.filter_manager.common_filters import CommonFilters
from sqlalchemy import cast
from sqlalchemy.sql.sqltypes import Time

class GamesFilterManager(BaseFilterManager, CommonFilters):

    @classmethod
    def apply_sport_filter(cls, query: Query, value: int) -> Query:
        return super().apply_sport_filter(query, Games, value)

    @staticmethod
    def apply_status_filter(query: Query, value: str) -> Query:
        return query.filter(Games.status == value)

    @staticmethod
    def apply_time_from_filter(query: Query, value: str) -> Query:
        return query.filter(cast(Games.time, Time) >= value)

    @staticmethod
    def apply_time_to_filter(query: Query, value: str) -> Query:
        return query.filter(cast(Games.time, Time) <= value)

    @staticmethod
    def apply_date_from(query: Query, value: str) -> Query:
        return query.filter(cast(Games.date, Date) >= value)

    @staticmethod
    def apply_date_to(query: Query, value: str) -> Query:
        return query.filter(cast(Games.date, Date) <= value)

    @classmethod
    def apply_country_filter(cls, query: Query, value: int) -> Query:
        return super().apply_country_filter(query, Games, value)

    @classmethod
    def apply_league_filter(cls, query: Query, value: int) -> Query:
        return super().apply_league_filter(query, Games, value)

    @staticmethod
    def apply_team_away_filter(query: Query, value: str) -> Query:
        return query.filter(Games.team_away_id == value)

    @staticmethod
    def apply_team_home_filter(query: Query, value: str) -> Query:
        return query.filter(Games.team_home_id == value)

    FILTERS = {
        "sport": apply_sport_filter,
        "date_from": apply_date_from,
        "date_to": apply_date_to,
        "team_away": apply_team_away_filter,
        "team_home": apply_team_home_filter,
        "country_id": apply_country_filter,
        "league_id": apply_league_filter,
        "status": apply_status_filter,
        "time_to": apply_time_to_filter,
        "time_from": apply_time_from_filter,
    }