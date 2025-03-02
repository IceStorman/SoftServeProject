from dto.api_input import TeamsLeagueDTO
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from database.models import TeamIndex, Sport, League, Country
from dto.api_output import TeamsLeagueOutput
from logger.logger import Logger
from sqlalchemy import func
from service.api_logic.filter_manager.filter_manager_factory import FilterManagerFactory

class TeamsService:
    def __init__(self, teams_dal):
        self._teams_dal = teams_dal
        self._logger = Logger("logger", "all.log").logger

    def get_teams(self, filters_dto):

        query = self._teams_dal.get_query(TeamIndex)

        query = FilterManagerFactory.apply_filters(TeamIndex, query, filters_dto)
        count = query.count()

        teams = self._teams_dal.execute_query(query)
        schema = TeamsLeagueOutput(many=True)
        team = schema.dump(teams)
        return {
            "count": count,
            "teams": team,
        }



