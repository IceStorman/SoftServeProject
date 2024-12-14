from flask import Blueprint, request, jsonify
from service.api_logic.games_logic import get_stream_info_today, get_stream_info_for_sport, get_games_today
from database.session import SessionLocal
from api.routes.cache import cache
from api.routes.scripts import get_error_response, get_cache_key, post_cache_key
from exept.exeptions import DatabaseConnectionError
from api.routes.dto import GamesDTO

session = SessionLocal()
games_app = Blueprint('games_app', __name__)


@games_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    response = {"error in data base": str(e)}
    return get_error_response(response, 503)


# @games_app.route('/', methods=['GET'])
# @cache.cached(60*1.3)
# def get_stream_info_today1_endpoint():
#     try:
#         games = get_stream_info_today(session)
#         return games
#     except Exception as e:
#         response = {"error in service": str(e)}
#         return get_error_response(response, 500)
#
#
# @games_app.route('/<sport_type>', methods=['GET'])
# @cache.cached(60*1.3, key_prefix=get_cache_key)
# def get_sport_stream_info_today1_endpoint(sport_type):
#     try:
#         games = get_stream_info_for_sport(session, sport_type)
#         return games
#     except Exception as e:
#         response = {"error in service": str(e)}
#         return get_error_response(response, 500)


@games_app.route('/', methods=['GET'])
@cache.cached(60*1.3)
def get_stream_info_for_main1_endpoint():
    try:
        dto = GamesDTO()
        games = get_games_today(session, 6, dto)
        response_data = [game.dict() for game in games]
        return jsonify(response_data), 200
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@games_app.route('/filter', methods=['POST'])
@cache.cached(60*1.3, key_prefix=post_cache_key)
def get_stream_info_for_main_endpoint():
    try:
        data = request.get_json()
        dto = GamesDTO(**data)
        games = get_games_today(session, 6, dto)
        response_data = [game.dict() for game in games]

        return jsonify(response_data), 200
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)
