from sqlalchemy.orm import Query
from database.models import TeamIndex, League
from service.api_logic.scripts import get_sport_by_name
from service.api_logic.filter_manager.base_filter_manager import BaseFilterManager

class TeamsFilterManager(BaseFilterManager):

    @classmethod
    def apply_sport_filter(cls, query: Query, value: int) -> Query:
        return query.filter(TeamIndex.sport_id == value)

    @staticmethod
    def apply_name_filter(query: Query, value: str) -> Query:
        return query.filter(TeamIndex.name.ilike(f"%{value}%"))

    @staticmethod
    def apply_league_filter(query: Query, value: int) -> Query:
        return query.join(League, TeamIndex.league_id == League.league_id).filter(League.api_id == value)

    FILTERS = {
        "sport_id": apply_sport_filter,
        "name": apply_name_filter,
        "league_id": apply_league_filter,
    }