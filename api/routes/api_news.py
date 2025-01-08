import logging
from flask import Blueprint,request
from service.api_logic.news_logic import get_news_by_count, get_latest_sport_news, get_popular_news, get_news_by_id
from api.routes.cache import cache
from api.routes.scripts import get_cache_key
from exept.handle_exeptions import get_error_response
from exept.exeptions import DatabaseConnectionError
from logger.logger import get_logger, log_function_call

api_routes_logger = get_logger("api_routes_loger", "api_routes.log")

news_app = Blueprint('news', __name__)
COUNT_NEWS = 5

@news_app.errorhandler(DatabaseConnectionError)
@log_function_call(api_routes_logger)
def handle_db_timeout_error(e):
    api_routes_logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@news_app.route('/recent', methods=['GET'])
@cache.cached(timeout=60*60)
@log_function_call(api_routes_logger)
def get_recent_news_endpoint():
    try:
        recent_news = get_news_by_count(COUNT_NEWS)
        return recent_news
    except Exception as e:
        get_error_response(e)


@news_app.route('/<sport_type>', methods=['GET'])
@cache.cached(timeout=60*60, key_prefix=get_cache_key)
@log_function_call(api_routes_logger)
def get_sport_news_endpoint(sport_type):
    try:
        sport_news = get_latest_sport_news(COUNT_NEWS, sport_type)
        return sport_news
    except Exception as e:
        get_error_response(e)


@news_app.route('/popular', methods=['GET'])
@cache.cached(timeout=60*3)
@log_function_call(api_routes_logger)
def get_popular_news_endpoint():
    try:
        popular_news = get_popular_news(COUNT_NEWS)
        return popular_news
    except Exception as e:
        get_error_response(e)


@news_app.route('/article', methods=['POST'])
@log_function_call(api_routes_logger)
def specific_article():

    try:
        article = request.get_json()
        news_id=article['blob_id']
        response = get_news_by_id(news_id)
        return response
    except Exception as e:
        get_error_response(e)


    




