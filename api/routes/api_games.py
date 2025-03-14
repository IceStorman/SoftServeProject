from flask import Blueprint, request
from dto.api_input import GamesDTO
from dto.pagination import Pagination
from service.api_logic.games_logic import get_games_today
from api.routes.cache import cache
from api.routes.scripts import  post_cache_key
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from exept.handle_exeptions import get_custom_error_response
from logger.logger import Logger

logger = Logger("logger", "all.log")

CACHE_TIMEOUT_SECONDS = 60 * 1.3
games_app = Blueprint('games_app', __name__)


@games_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@games_app.route('/today', methods=['POST'])
@cache.cached(CACHE_TIMEOUT_SECONDS)
@logger.log_function_call()
def get_stream_info_endpoint():
    try:
        data = request.get_json()
        dto = GamesDTO().load(data)
        pagination = Pagination(**data)
        games = get_games_today(dto, pagination)
        return games
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)


@games_app.route('/specific', methods=['POST'])
@cache.cached(CACHE_TIMEOUT_SECONDS, key_prefix=post_cache_key)
@logger.log_function_call()
def get_stream_info_with_filters_endpoint():
    try:
        data = request.get_json()
        dto = GamesDTO().load(data)
        pagination = Pagination(**data)
        games = get_games_today(dto, pagination)
        return games
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)
