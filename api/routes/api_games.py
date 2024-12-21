from flask import Blueprint, request
from dto.api_input import GamesDTO
from service.api_logic.games_logic import get_games_today
from database.session import SessionLocal
from api.routes.cache import cache
from api.routes.scripts import get_error_response, post_cache_key
from exept.exeptions import DatabaseConnectionError

session = SessionLocal()
games_app = Blueprint('games_app', __name__)


@games_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    response = {"error in data base": str(e)}
    return get_error_response(response, 503)


@games_app.route('/', methods=['GET'])
@cache.cached(60*1.3)
def get_stream_info_for_main1_endpoint():
    try:
        dto = GamesDTO()
        games = get_games_today(session, dto)
        return games
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@games_app.route('/filter', methods=['POST'])
@cache.cached(60*1.3, key_prefix=post_cache_key)
def get_stream_info_for_main_endpoint():
    try:
        data = request.get_json()
        dto = GamesDTO(**data)
        games = get_games_today(session, dto)
        return games
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)