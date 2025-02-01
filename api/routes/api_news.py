from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request, jsonify
from api.container.container import Container
from service.api_logic.news_logic import get_news_by_count, get_latest_sport_news, get_popular_news, get_news_by_id
from api.routes.cache import cache
from api.routes.scripts import get_cache_key
from exept.handle_exeptions import get_error_response
from exept.exeptions import DatabaseConnectionError
from logger.logger import Logger
from service.api_logic.recommendation_logic import RecommendationService
from service.api_logic.websocket import connected_users, socketio

api_routes_logger = Logger("api_routes_logger", "api_routes_logger.log")

news_app = Blueprint('news', __name__)
COUNT_NEWS = 5

@news_app.errorhandler(DatabaseConnectionError)
@api_routes_logger.log_function_call()
def handle_db_timeout_error(e):
    api_routes_logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@news_app.route('/recent', methods=['GET'])
@cache.cached(timeout=60*60)
@api_routes_logger.log_function_call()
def get_recent_news_endpoint():
    try:
        recent_news = get_news_by_count(COUNT_NEWS)
        return recent_news
    except Exception as e:
        api_routes_logger.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@news_app.route('/<sport_type>', methods=['GET'])
@cache.cached(timeout=60*60, key_prefix=get_cache_key)
@api_routes_logger.log_function_call()
def get_sport_news_endpoint(sport_type):
    try:
        sport_news = get_latest_sport_news(COUNT_NEWS, sport_type)
        return sport_news
    except Exception as e:
        api_routes_logger.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@news_app.route('/popular', methods=['GET'])
@cache.cached(timeout=60*3)
@api_routes_logger.log_function_call()
def get_popular_news_endpoint():
    try:
        popular_news = get_popular_news(COUNT_NEWS)
        return popular_news
    except Exception as e:
        api_routes_logger.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@news_app.route('/article', methods=['POST'])
@api_routes_logger.log_function_call()
def specific_article():

    try:
        article = request.get_json()
        news_id=article['blob_id']
        response = get_news_by_id(news_id)
        return response
    except Exception as e:
        api_routes_logger.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@news_app.route("/recommendations", methods=["GET"])
@inject
def generate_recommendations(service: RecommendationService = Provide[Container.recommendation_service]):
    try:
        service.recommendations()
        return jsonify({"status": "Processing recommendations"}), 202
    except Exception as e:
        api_routes_logger.error(f"Error in RECOMMENDATIONS: {str(e)}")

    




