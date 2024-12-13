from flask import Blueprint
from service.api_logic.news_logic import get_news_by_count, get_latest_sport_news, get_popular_news
from database.session import SessionLocal
from api.routes.cache import cache
from api.routes.scripts import make_cache_key, get_error_response, check_positive_param
from exept.exeptions import SoftServeException
session = SessionLocal()
news_app = Blueprint('news', __name__)


@news_app.errorhandler(SoftServeException)
def handle_db_timeout_error(e):
    response = e.get_response()
    return get_error_response(response, response.status_code)


@news_app.route('/recent', methods=['GET'])
@cache.cached(timeout=60*60)
def get_recent_news_endpoint():
    try:
        recent_news = get_news_by_count(5, session)
        return recent_news
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)

@news_app.route('/<sport_type>', methods=['GET'])
@cache.cached(timeout=60*60, key_prefix=make_cache_key)
def get_sport_news_endpoint(sport_type):
    try:
        recent_news = get_latest_sport_news(5, sport_type, session)
        return recent_news
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@news_app.route('/popular', methods=['GET'])
@cache.cached(timeout=60*3)
def get_popular_news_endpoint():
    try:
        recent_news = get_popular_news(5, session)
        return recent_news
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)



