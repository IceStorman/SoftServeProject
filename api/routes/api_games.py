from flask import Blueprint
from service.api_logic.games_logic import get_stream_info_today, get_stream_info_for_sport
from database.session import SessionLocal
from api.routes.cache import cache
from api.routes.scripts import get_error_response, make_cache_key

session = SessionLocal()
games_app = Blueprint('games_app', __name__)

@games_app.route('/', methods=['GET'])
@cache.cached(60*1.3)
def get_stream_info_today_endpoint():
   try:
      games = get_stream_info_today(session)
      return games, 200
   except Exception as e:
      return get_error_response(e), 500


@games_app.route('/<sport_type>', methods=['GET'])
@cache.cached(60*1.3, key_prefix=make_cache_key)
def get_sport_stream_info_today_endpoint(sport_type):
    try:
       games = get_stream_info_for_sport(session, sport_type)
       return games, 200
    except Exception as e:
       return get_error_response(e), 500