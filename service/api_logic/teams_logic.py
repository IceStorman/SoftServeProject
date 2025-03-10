from dto.api_input import TeamsLeagueDTO
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from database.models import TeamIndex, Sport, League, Country
from dto.api_output import TeamsLeagueOutput, ListResponseDTO
from logger.logger import Logger
from sqlalchemy import func
from service.api_logic.filter_manager.filter_manager_strategy import FilterManagerStrategy

class TeamsService:
    def __init__(self, teams_dal):
        self._teams_dal = teams_dal
        self._logger = Logger("logger", "all.log").logger

    def get_teams_filtered(self, filters_dto):
        query = self._teams_dal.get_base_query(TeamIndex)

        query, count = FilterManagerStrategy.apply_filters(TeamIndex, query, filters_dto)

        teams = self._teams_dal.execute_query(query)
        teams_output = TeamsLeagueOutput(many=True)
        team = teams_output.dump(teams)

        response_dto = ListResponseDTO()

        return response_dto.dump({"items": team, "count": count})



