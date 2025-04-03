from flask import request
from flask_smorest import Blueprint
from dto.api_input import SearchDTO
from api.routes.cache import cache
from api.routes.scripts import  post_cache_key
from dto.api_output import ListResponseDTO
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from exept.handle_exeptions import get_custom_error_response
from logger.logger import Logger
from api.container.container import Container
from dependency_injector.wiring import inject, Provide
from service.api_logic.games_logic import GamesService

logger = Logger("logger", "all.log")

CACHE_TIMEOUT_SECONDS = 60 * 1.3
games_app = Blueprint('games_app', __name__, description="Games information", url_prefix='/games')


@games_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@games_app.route('/search', methods=['POST'])
@cache.cached(CACHE_TIMEOUT_SECONDS, key_prefix=post_cache_key)
@inject
@logger.log_function_call()
@games_app.arguments(SearchDTO)
@games_app.response(200, ListResponseDTO(many=True))
def get_games_info_with_filters_endpoint(games_service: GamesService = Provide[Container.games_service]):
    try:
        data = request.get_json()
        dto = SearchDTO().load(data)
        games = games_service.get_games_today(dto)
        return games
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)
