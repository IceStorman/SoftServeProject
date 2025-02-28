from database.models import League
from sqlalchemy.orm import Query
from service.api_logic.scripts import get_sport_by_name

class CommonFilters():

    @staticmethod
    def apply_sport_filter(query: Query, model, value: int) -> Query:
       return query.filter(getattr(model, "sport_id") == value)

    @staticmethod
    def apply_country_filter(query: Query, model, value: int) -> Query:
        return query.filter(getattr(model, "country_id") == value)

    @staticmethod
    def apply_league_filter(query: Query, model, value: int) -> Query:
        return query.join(League, model.league_id == League.league_id).filter(League.api_id == value)

    @staticmethod
    def apply_name_filter(query: Query, model, value: str) -> Query:
        return query.filter(getattr(model, "name").ilike(f"%{value}%"))

