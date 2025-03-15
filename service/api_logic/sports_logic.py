from sqlalchemy import func
from database.models import Sport, League, Country
from dto.api_output import SportsLeagueOutput, SportsOutput, ListResponseDTO
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from logger.logger import Logger
from service.api_logic.filter_manager.filter_manager_strategy import FilterManagerStrategy

class SportService:
    def __init__(self, sports_dal, leagues_dal):
        self._sports_dal = sports_dal
        self._leagues_dal = leagues_dal
        self._logger = Logger("logger", "all.log").logger

    def get_all_sports(self):
        sports_query = self._sports_dal.get_base_query(Sport)
        execute_query = self._sports_dal.query_output(sports_query)
        sport_output = SportsOutput(many=True)
        return sport_output.dump(execute_query)

    def search_leagues(self, filters_dto):

        query = self._leagues_dal.get_base_query(League)

        filtered_query, count = FilterManagerStrategy.apply_filters(League, query, filters_dto)

        execute_query = self._leagues_dal.query_output(filtered_query)

        sport_output = SportsLeagueOutput(many=True)
        leagues = sport_output.dump(execute_query)

        response_dto = ListResponseDTO()

        return response_dto.dump({"items": leagues, "count": count})





