import logging
from flask import Blueprint, request
from dto.api_input import GamesDTO
from dto.pagination import Pagination
from service.api_logic.games_logic import get_games_today
from api.routes.cache import cache
from api.routes.scripts import  post_cache_key
from exept.exeptions import DatabaseConnectionError
from exept.handle_exeptions import get_error_response
from api.routes.api_routes_logging import setup_logger

setup_logger()

CACHE_TIMEOUT_SECONDS = 60 * 1.3
games_app = Blueprint('games_app', __name__)


@games_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logging.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@games_app.route('/today', methods=['POST'])
@cache.cached(CACHE_TIMEOUT_SECONDS)
def get_stream_info_endpoint():
    try:
        logging.info(f"GET request to / from {request.remote_addr}")
        data = request.get_json()
        dto = GamesDTO().load(data)
        pagination = Pagination(**data)
        games = get_games_today(dto, pagination)
        logging.info(f"Successfully retrieved games.")
        return games
    except Exception as e:
        logging.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@games_app.route('/specific', methods=['POST'])
@cache.cached(CACHE_TIMEOUT_SECONDS, key_prefix=post_cache_key)
def get_stream_info_with_filters_endpoint():
    try:
        logging.info(f"GET request to / from {request.remote_addr}")
        data = request.get_json()
        dto = GamesDTO().load(data)
        pagination = Pagination(**data)
        games = get_games_today(dto, pagination)
        logging.info(f"Successfully retrieved games.")
        return games
    except Exception as e:
        logging.error(f"Error in GET /: {str(e)}")
        get_error_response(e)
