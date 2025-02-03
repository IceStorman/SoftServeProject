from flask import Blueprint, request
from exept.handle_exeptions import get_custom_error_response
from service.api_logic.sports_logic import get_all_sports, get_all_leagues_by_sport, search_leagues
from api.routes.scripts import post_cache_key
from api.routes.cache import cache
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from dto.api_input import SportsLeagueDTO, SearchDTO
from dto.pagination import Pagination
from logger.logger import Logger

logger = Logger("logger", "all.log")

sports_app = Blueprint('sports', __name__)


@sports_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@sports_app.route('/all', methods=['GET'])
@cache.cached(timeout=60*60)
@logger.log_function_call()
def get_all_sports_endpoint():
    try:
        all_sports = get_all_sports()
        return all_sports
    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        get_custom_error_response(e)


@sports_app.route('/league', methods=['POST'])
@cache.cached(timeout=60*60, key_prefix=post_cache_key)
@logger.log_function_call()
def get_all_leagues_endpoint():
    try:
        data = request.get_json()
        dto = SportsLeagueDTO().load(data)
        pagintion = Pagination(**data)
        league_sports = get_all_leagues_by_sport(dto, pagintion)
        return league_sports
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)


@sports_app.route('/league/search', methods=['POST'])
@logger.log_function_call()
def search_countries():
    try:
        data = request.get_json()
        dto = SearchDTO().load(data)
        pagintion = Pagination(**data)
        leagues = search_leagues(dto, pagintion)
        return leagues
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)

