from flask import Blueprint
from service.api_logic.games_logic import get_stream_info_today, get_stream_info_for_sport
from database.session import SessionLocal
from api.routes.cache import cache
from api.routes.scripts import get_error_response, make_cache_key
from exept.exeptions import DatabaseConnectionError

session = SessionLocal()
games_app = Blueprint('games_app', __name__)


@games_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    response = {"error in data base": str(e)}
    return get_error_response(response, 503)


@games_app.route('/', methods=['GET'])
@cache.cached(60*1.3)
def get_stream_info_today_endpoint():
    try:
        games = get_stream_info_today(session)
        return games
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@games_app.route('/<sport_type>', methods=['GET'])
@cache.cached(60*1.3, key_prefix=make_cache_key)
def get_sport_stream_info_today_endpoint(sport_type):
    try:
        games = get_stream_info_for_sport(session, sport_type)
        return games
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)