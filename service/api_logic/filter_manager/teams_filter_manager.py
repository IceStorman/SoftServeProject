from sqlalchemy.orm import Query
from database.models import TeamIndex
from service.api_logic.scripts import get_sport_by_name
from service.api_logic.filter_manager.base_filter_manager import BaseFilterManager
from service.api_logic.filter_manager.common_filters import CommonFilters

class TeamsFilterManager(BaseFilterManager, CommonFilters):

    @classmethod
    def apply_sport_filter(cls, query: Query, value: int) -> Query:
        return super().apply_sport_filter(query, TeamIndex, value)

    @classmethod
    def apply_name_filter(cls, query: Query, value: str) -> Query:
        return super().apply_name_filter(query, TeamIndex, value)

    @classmethod
    def apply_league_filter(cls, query: Query, value: str) -> Query:
        return super().apply_league_filter(query, TeamIndex, value)

    FILTERS = {
        "sport_id": apply_sport_filter,
        "name": apply_name_filter,
        "league_id": apply_league_filter,
    }