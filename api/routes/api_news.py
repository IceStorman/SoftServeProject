from flask import Blueprint, jsonify, request
from service.api_logic.news_logic import get_news_by_count, get_latest_sport_news
from database.session import SessionLocal
from api.routes.cache import cache

session = SessionLocal()
news_app = Blueprint('news', __name__)

def make_cache_key():
   sport_type = request.view_args.get('sport_type')  # Отримання значення sport_type із запиту
   return f"sport_stream_{sport_type}"


@news_app.route('/recent', methods=['GET'])
@cache.cached(timeout=60*60)
def get_recent_news_endpoint():
    try:
        recent_news = get_news_by_count(5, session)
        return recent_news, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@news_app.route('/<sport_type>', methods=['GET'])
@cache.cached(timeout=60*60, key_prefix=make_cache_key)
def get_sport_news_endpoint(sport_type):
    try:
        recent_news = get_latest_sport_news(5, sport_type, session)
        return recent_news, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500