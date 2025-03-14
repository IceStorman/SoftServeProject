from sqlalchemy.orm import Query
from database.models import League, Country
from service.api_logic.filter_manager.base_filter_manager import BaseFilterManager

class LeagueFilterManager(BaseFilterManager):

    @staticmethod
    def apply_sport_filter(query: Query, value: int) -> Query:
        return query.filter(League.sport_id == value)

    @staticmethod
    def apply_country_filter(query: Query, value: int) -> Query:
        return query.join(Country, League.country_id == Country.country_id).filter(Country.api_id == value)

    @staticmethod
    def apply_name_filter(query: Query, value: str) -> Query:
        return query.filter(League.name.ilike(f"%{value}%"))

    FILTERS = {
        "sport_id": apply_sport_filter,
        "country_id": apply_country_filter,
        "name": apply_name_filter,
    }
