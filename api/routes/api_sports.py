import logging
from flask import Blueprint, request
from exept.handle_exeptions import get_error_response
from service.api_logic.sports_logic import get_all_sports, get_all_leagues_by_sport, search_leagues
from api.routes.scripts import post_cache_key
from api.routes.cache import cache
from exept.exeptions import DatabaseConnectionError
from dto.api_input import SportsLeagueDTO, SearchDTO
from dto.pagination import Pagination
from logger.logger import Logger

api_routes_logger = Logger("api_routes_logger", "api_routes_logger.log")

sports_app = Blueprint('sports', __name__)


@sports_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    api_routes_logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@sports_app.route('/all', methods=['GET'])
@cache.cached(timeout=60*60)
@api_routes_logger.log_function_call()
def get_all_sports_endpoint():
    try:
        all_sports = get_all_sports()
        return all_sports
    except Exception as e:
        api_routes_logger.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@sports_app.route('/league', methods=['POST'])
@cache.cached(timeout=60*60, key_prefix=post_cache_key)
@api_routes_logger.log_function_call()
def get_all_leagues_endpoint():
    try:
        data = request.get_json()
        dto = SportsLeagueDTO().load(data)
        pagintion = Pagination(**data)
        league_sports = get_all_leagues_by_sport(dto, pagintion)
        return league_sports
    except Exception as e:
        api_routes_logger.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@sports_app.route('/league/search', methods=['POST'])
@api_routes_logger.log_function_call()
def search_countries():
    try:
        data = request.get_json()
        dto = SearchDTO().load(data)
        pagintion = Pagination(**data)
        leagues = search_leagues(dto, pagintion)
        return leagues
    except Exception as e:
        api_routes_logger.error(f"Error in GET /: {str(e)}")
        get_error_response(e)

