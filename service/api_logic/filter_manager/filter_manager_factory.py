from service.api_logic.filter_manager.games_filter_manager import GamesFilterManager
from service.api_logic.filter_manager.league_filter_manager import LeagueFilterManager
from service.api_logic.filter_manager.news_filter_manager import NewsFilterManager
from sqlalchemy.orm import Query

class FilterManagerFactory:

    MANAGERS = {
        "News": NewsFilterManager,
        "Games": GamesFilterManager,
        "League": LeagueFilterManager,
    }

    @classmethod
    def apply_filters(cls, model, query: Query, filters, session) -> Query:

        table_name = model.__tablename__

        if table_name not in cls.MANAGERS:
            raise ValueError(f"No filter manager found for model: {table_name}")

        filter_manager = cls.MANAGERS[table_name]
        return filter_manager.apply_filters(query, filters, session)