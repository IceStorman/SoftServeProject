from flask import request, jsonify
from flask_smorest import Blueprint

from dto.api_output import SportsOutput, ListResponseDTO
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

sports_app = Blueprint('sports', __name__, description="Sports and Leagues information", url_prefix='/sports')


@sports_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@sports_app.route('/all', methods=['GET'])
@inject
@cache.cached(timeout=60*60)
@logger.log_function_call()
@sports_app.response(200, SportsOutput(many=True))
def get_all_sports_endpoint(league_service: SportService = Provide[Container.sports_service]):
    """Get all sports information"""
    try:
        return jsonify(league_service.get_all_sports())

    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        return get_custom_error_response(e)


@sports_app.route('/league/search', methods=['POST'])
@inject
@logger.log_function_call()
@sports_app.arguments(SearchDTO)
@sports_app.response(200, ListResponseDTO(many=True))
def search_leagues(dto: SearchDTO, league_service: SportService = Provide[Container.sports_service]):
    """Get all leagues information by filters"""
    try:
        return jsonify(league_service.search_leagues(dto))

    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)

