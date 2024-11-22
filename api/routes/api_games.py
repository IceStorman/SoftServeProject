from flask import Blueprint, jsonify, request
from service.api_logic.games_logic import get_stream_info_today, get_stream_info_for_sport
from database.session import SessionLocal
from api.routes.cache import cache

session = SessionLocal()
games_app = Blueprint('games_app', __name__)

def make_cache_key():
   sport_type = request.view_args.get('sport_type')
   return f"sport_stream_{sport_type}"


@games_app.route('/', methods=['GET'])
@cache.cached(60*1.3)
def get_stream_info_today_endpoint():
   try:
      games = get_stream_info_today(session)
      return games, 200
   except Exception as e:
      return jsonify({"error": str(e)}), 500


@games_app.route('/<sport_type>', methods=['GET'])
@cache.cached(60*1.3, key_prefix=make_cache_key)
def get_sport_stream_info_today_endpoint(sport_type):
    try:
       games = get_stream_info_for_sport(session, sport_type)
       return games, 200
    except Exception as e:
       return jsonify({"error": str(e)}), 500