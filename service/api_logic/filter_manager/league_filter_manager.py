from sqlalchemy.orm import Query
from database.models import League
from service.api_logic.filter_manager.base_filter_manager import BaseFilterManager
from service.api_logic.filter_manager.common_filters import CommonFilters

class LeagueFilterManager(BaseFilterManager, CommonFilters):

    FILTERS = {
        "sport_id": "apply_sport_filter",
        "country_id": "apply_country_filter",
        "name":"apply_name_filter",
    }

    @classmethod
    def apply_sport_filter(cls, query: Query, value: str) -> Query:
        return super().apply_sport_filter(query, League, value)

    @classmethod
    def apply_country_filter(cls, query: Query, value: int) -> Query:
        return super().apply_country_filter(query, League, value)

    @classmethod
    def apply_name_filter(cls, query: Query, value: str) -> Query:
        return super().apply_name_filter(query, League, value)