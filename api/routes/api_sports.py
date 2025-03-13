from flask import Blueprint, request
from exept.handle_exeptions import get_custom_error_response
from api.routes.scripts import post_cache_key
from api.routes.cache import cache
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from dto.api_input import SportsLeagueDTO, SearchDTO
from dto.pagination import Pagination
from logger.logger import Logger
from dependency_injector.wiring import Provide, inject
from api.container.container import Container
from service.api_logic.sports_logic import SportService

logger = Logger("logger", "all.log")

sports_app = Blueprint('sports', __name__)


@sports_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@sports_app.route('/all', methods=['GET'])
@inject
@cache.cached(timeout=60*60)
@logger.log_function_call()
def get_all_sports_endpoint(league_service: SportService = Provide[Container.sports_service]):
    try:
        all_sports = league_service.get_all_sports()
        return all_sports
    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        get_custom_error_response(e)


@sports_app.route('/league/search', methods=['POST'])
@inject
@logger.log_function_call()
def search_leagues(league_service: SportService = Provide[Container.sports_service]):
    try:
        data = request.get_json()
        dto = SearchDTO().load(data)
        leagues = league_service.search_leagues(dto)
        return leagues
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)

