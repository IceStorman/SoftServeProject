from flask import Blueprint, request
from exept.handle_exeptions import get_error_response
from service.api_logic.sports_logic import get_all_sports, get_all_leagues_by_sport, search_leagues
from api.routes.scripts import post_cache_key
from api.routes.cache import cache
from exept.exeptions import DatabaseConnectionError
from dto.api_input import SportsLeagueDTO, SearchDTO

sports_app = Blueprint('sports', __name__)


@sports_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    response = {"error in data base": str(e)}
    return response


@sports_app.route('/all', methods=['GET'])
@cache.cached(timeout=60*60)
def get_all_sports_endpoint():
    try:
        all_sports = get_all_sports()
        return all_sports
    except Exception as e:
        get_error_response(e)


@sports_app.route('/league', methods=['POST'])
@cache.cached(timeout=60*60, key_prefix=post_cache_key)
def get_all_leagues_endpoint():
    try:
        data = request.get_json()
        dto = SportsLeagueDTO(**data)
        league_sports = get_all_leagues_by_sport(dto)
        return league_sports
    except Exception as e:
        get_error_response(e)


@sports_app.route('/league/search', methods=['POST'])
def search_countries():
    try:
        data = request.get_json()
        dto = SearchDTO(**data)
        leagues = search_leagues(dto)
        return leagues
    except Exception as e:
        get_error_response(e)

