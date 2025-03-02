from sqlalchemy import func
from database.models import Sport, League, Country
from dto.api_output import SportsLeagueOutput, SportsOutput
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from logger.logger import Logger
from service.api_logic.filter_manager.filter_manager_factory import FilterManagerFactory

class SportService:
    def __init__(self, sports_dal, leagues_dal):
        self._sports_dal = sports_dal
        self._leagues_dal = leagues_dal
        self._logger = Logger("logger", "all.log").logger

    def get_all_sports(self):
        sports_query = self._sports_dal.get_query(Sport)
        execute_query = self._sports_dal.execute_query(sports_query)
        schema = SportsOutput(many=True)
        return schema.dump(execute_query)

    def search_leagues(self, filters_dto):

        query = self._leagues_dal.get_query(League)

        model_aliases = {
            "leagues": League,
            "countries": Country,
        }

        filtered_query = FilterManagerFactory.apply_filters(League, query, filters_dto)
        count = filtered_query.count()

        execute_query = self._leagues_dal.execute_query(filtered_query)

        sport_output = SportsLeagueOutput(many=True)
        leagues = sport_output.dump(execute_query)
        return {
            "count": count,
            "leagues": leagues,
        }





