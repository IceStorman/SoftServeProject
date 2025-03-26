from database.models import Players
from dto.api_output import ListResponseDTO, PlayersOutput
from logger.logger import Logger
from service.api_logic.filter_manager.filter_manager_strategy import FilterManagerStrategy

class PlayerService:
    def __init__(self, players_dal):
        self.__players_dal = players_dal
        self.__logger = Logger("logger", "all.log").logger

    def get_teams_filtered(self, filters_dto):
        query = self.__players_dal.get_base_query(Players)

        query, count = FilterManagerStrategy.apply_filters(Players, query, filters_dto)

        players = self.__players_dal.query_output(query)
        players_output = PlayersOutput(many=True)
        player = players_output.dump(players)

        response_dto = ListResponseDTO()

        return response_dto.dump({"items": player, "count": count})



