import logging
from flask import Blueprint, request
from dto.api_input import GamesDTO
from dto.pagination import Pagination
from service.api_logic.games_logic import get_games_today
from api.routes.cache import cache
from api.routes.scripts import  post_cache_key
from exept.exeptions import DatabaseConnectionError
from exept.handle_exeptions import get_error_response
from logger.logger import Logger

api_routes_logger = Logger("api_routes_logger", "api_routes_logger.log")

CACHE_TIMEOUT_SECONDS = 60 * 1.3
games_app = Blueprint('games_app', __name__)


@games_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    api_routes_logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@games_app.route('/today', methods=['POST'])
@cache.cached(CACHE_TIMEOUT_SECONDS)
@api_routes_logger.log_function_call()
def get_stream_info_endpoint():
    try:
        data = request.get_json()
        dto = GamesDTO().load(data)
        pagination = Pagination(**data)
        games = get_games_today(dto, pagination)
        return games
    except Exception as e:
        api_routes_logger.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@games_app.route('/specific', methods=['POST'])
@cache.cached(CACHE_TIMEOUT_SECONDS, key_prefix=post_cache_key)
@api_routes_logger.log_function_call()
def get_stream_info_with_filters_endpoint():
    try:
        data = request.get_json()
        dto = GamesDTO().load(data)
        pagination = Pagination(**data)
        games = get_games_today(dto, pagination)
        return games
    except Exception as e:
        api_routes_logger.error(f"Error in GET /: {str(e)}")
        get_error_response(e)
