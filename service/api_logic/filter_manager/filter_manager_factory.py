from service.api_logic.filter_manager.news_filter_manager import NewsFilterManager
from sqlalchemy.orm import Query

class FilterManagerFactory:

    MANAGERS = {
        "News": NewsFilterManager,
    }

    @classmethod
    def apply_filters(cls, model, query: Query, filters: dict, session) -> Query:

        table_name = model.__tablename__

        if table_name not in cls.MANAGERS:
            raise ValueError(f"No filter manager found for model: {table_name}")

        filter_manager = cls.MANAGERS[table_name]
        return filter_manager.apply_filters(query, filters, session)