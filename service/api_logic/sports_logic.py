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
        sports = self._sports_dal.get_query()
        execute_query = self._sports_dal.execute_query(sports)
        schema = SportsOutput(many=True)
        return schema.dump(execute_query)

    def search_leagues(self, filters_dto, pagination: Pagination):

        query = self._leagues_dal.get_query()

        model_aliases = {
            "leagues": League,
            "countries": Country,
        }

        filtered_query = FilterManagerFactory.apply_filters(League, query, filters_dto)
        count = filtered_query.count()

        offset, limit = pagination.get_pagination()
        if offset is not None and limit is not None:
            filtered_query = filtered_query.offset(offset).limit(limit)

        execute_query = self._leagues_dal.execute_query(filtered_query)

        schema = SportsLeagueOutput(many=True)
        leagues = schema.dump(execute_query)
        return {
            "count": count,
            "leagues": leagues,
        }





