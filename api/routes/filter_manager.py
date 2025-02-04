from sqlalchemy.orm import Query
from database.models import News
from service.api_logic.scripts import get_sport_by_name


class NewsFilterManager:

    FILTERS = {
        "title_contains": "apply_title_contains",
        "sport": "apply_sport_filter",
        "date_from": "apply_date_from",
        "date_to": "apply_date_to",
    }

    @staticmethod
    def apply_title_contains(query: Query, value: str) -> Query:
        return query.filter(News.blob_id.ilike(f"%{value}%"))

    @staticmethod
    def apply_sport_filter(query: Query, value: str, session) -> Query:
        sport = get_sport_by_name(session, value)
        return query.filter(News.sport_id == sport.sport_id)

    @staticmethod
    def apply_date_from(query: Query, value: str) -> Query:
        return query.filter(News.save_at >= value)

    @staticmethod
    def apply_date_to(query: Query, value: str) -> Query:
        return query.filter(News.save_at <= value)

    @classmethod
    def apply_filters(cls, query: Query, filters: dict, session) -> Query:
        for filter_name, filter_value in filters.items():
            if filter_name in cls.FILTERS and filter_value:
                filter_method = getattr(cls, cls.FILTERS[filter_name])
                if filter_name == "sport":
                    query = filter_method(query, filter_value, session)
                else:
                    query = filter_method(query, filter_value)
        return query
