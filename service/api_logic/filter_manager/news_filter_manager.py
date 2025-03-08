from sqlalchemy.orm import Query
from database.models import News, TeamInNews
from service.api_logic.filter_manager.base_filter_manager import BaseFilterManager
from service.api_logic.filter_manager.common_filters import CommonFilters
from sqlalchemy import desc, asc

class NewsFilterManager(BaseFilterManager, CommonFilters):

    @staticmethod
    def apply_title_contains(query: Query, value: str) -> Query:
        return query.filter(News.blob_id.ilike(f"%{value}%"))

    @staticmethod
    def apply_sport_filter(query: Query, value: int) -> Query:
        return query.filter(News.sport_id == value)

    @staticmethod
    def apply_date_from(query: Query, value: str) -> Query:
        return query.filter(cast(News.save_at, Date) >= value)

    @staticmethod
    def apply_date_to(query: Query, value: str) -> Query:
        return query.filter(cast(News.save_at, Date) <= value)

    @staticmethod
    def apply_team_filter(query: Query, value: str) -> Query:
        return query.join(TeamInNews, News.news_id == TeamInNews.news_id).filter(TeamInNews.name.ilike(f"%{value}%"))


    def apply_order_by_filter(self, query: Query, filters) -> Query:
        if filters.field and filters.order:
            order = asc if filters.order.lower() == "asc" else desc
            return self.apply_order_by(query, News, order, filters.field)
        return query

    FILTERS = {
        "title_contains": apply_title_contains,
        "sport_id": apply_sport_filter,
        "date_from": apply_date_from,
        "date_to": apply_date_to,
        "team": apply_team_filter,
        "order_by": apply_order_by_filter,
    }