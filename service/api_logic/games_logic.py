from dto.api_output import GameOutput
from dto.api_input import GamesDTO
from database.models import Games, Country, TeamIndex, League, Sport
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from sqlalchemy.orm import aliased
from logger.logger import Logger
from service.api_logic.filter_manager.filter_manager_factory import FilterManagerFactory

class GamesService:
    def __init__(self, games_dal):
        self._games_dal = games_dal
        self._logger = Logger("logger", "all.log").logger

    def get_games_today(self, filters_dto: GamesDTO(), pagination: Pagination):

        query = self._games_dal.get_query()

        filtered_query = FilterManagerFactory.apply_filters(Games, query, filters_dto)

        offset, limit = pagination.get_pagination()
        if offset is not None and limit is not None:
            filtered_query = filtered_query.offset(offset).limit(limit)

        games = self._games_dal.execute_query(filtered_query)

        schema = GameOutput(many=True)
        return schema.dump(games)


