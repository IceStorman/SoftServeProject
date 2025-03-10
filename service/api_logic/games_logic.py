from dto.api_output import GameOutput, ListResponseDTO
from dto.api_input import GamesDTO
from database.models import Games, Country, TeamIndex, League, Sport
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from sqlalchemy.orm import aliased
from logger.logger import Logger
from service.api_logic.filter_manager.filter_manager_strategy import FilterManagerStrategy

class GamesService:
    def __init__(self, games_dal):
        self._games_dal = games_dal
        self._logger = Logger("logger", "all.log").logger

    def get_games_today(self, filters_dto: GamesDTO()):

        query = self._games_dal.get_base_query(Games)

        filtered_query, count = FilterManagerStrategy.apply_filters(Games, query, filters_dto)

        games = self._games_dal.execute_query(filtered_query)

        game_output = GameOutput(many=True)

        games = game_output.dump(games)

        response_dto = ListResponseDTO()

        return response_dto.dump({"items": games, "count": count})


