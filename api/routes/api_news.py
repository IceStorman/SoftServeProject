from dependency_injector.wiring import Provide, inject
from flask import request
from flask_smorest import Blueprint
from flask_jwt_extended import get_jwt, jwt_required
from api.routes.cache import cache
from api.routes.scripts import get_cache_key, get_recommendation_key
from dto.api_output import OutputArrayOfArticles, OutputArticle, ListResponseDTO, OutputRecommendationList
from exept.handle_exeptions import get_custom_error_response, get_exception_error_response
from api.container.container import Container
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from logger.logger import Logger
from dto.api_input import SearchDTO
from exept.handle_exeptions import handle_exceptions
from service.api_logic.managers.recommendation_menager import RecommendationManager
from service.api_logic.news_logic import NewsService

logger = Logger("logger", "all.log")

news_app = Blueprint('news', __name__, description="News information", url_prefix='/news')
COUNT_NEWS = 5

@news_app.errorhandler(DatabaseConnectionError)
@logger.log_function_call()
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@news_app.route('/recent', methods=['GET'])
@cache.cached(timeout=60*60)
@inject
@handle_exceptions
@logger.log_function_call()
@news_app.response(200, OutputArrayOfArticles())
def get_recent_news_endpoint(service: NewsService = Provide[Container.news_service]):
    """Get all recent news information"""
    try:
        recent_news = service.get_news_by_count(COUNT_NEWS)
        return recent_news
    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        get_exception_error_response(e)


@news_app.route('/<sport_type>', methods=['GET'])
@cache.cached(timeout=60*60, key_prefix=get_cache_key)
@inject
@handle_exceptions
@logger.log_function_call()
@news_app.response(200, OutputArrayOfArticles())
def get_sport_news_endpoint(sport_type, service: NewsService = Provide[Container.news_service]):
    """Get all sport_type news information"""
    try:
        sport_news = service.get_latest_sport_news(COUNT_NEWS, sport_type)
        return sport_news
    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        get_custom_error_response(e)


@news_app.route('/article', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
@news_app.response(200, OutputArticle())
def specific_article(service: NewsService = Provide[Container.news_service]):
    """Get all news information"""
    try:
        article = request.get_json()
        news_id=article['blob_id']
        response = service.get_news_by_id(news_id)
        return response
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        return get_custom_error_response(e)


@news_app.route('/search', methods=['POST'])
@inject
@logger.log_function_call()
def get_filtered_news_endpoint(news_service: NewsService = Provide[Container.news_service]):
    try:
        filters = request.get_json() or {}
        dto = SearchDTO().load(filters)
        filtered_news = news_service.get_filtered_news(dto)

        return filtered_news

    except CustomQSportException as e:
        logger.error(f"Error in POST /filtered: {str(e)}")
        return get_custom_error_response(e)


@news_app.route("/recommendation", methods=["GET"])
@jwt_required()
@cache.cached(key_prefix=get_recommendation_key, timeout=60*60*2)
@inject
@handle_exceptions
@logger.log_function_call()
async def recommendations_for_user(recommendation_manager: RecommendationManager = Provide[Container.recommendation_manager]):
    """Get all recommendation news information"""
    try:
        decode_access_token = get_jwt()
        user_recommendations = recommendation_manager.get_recommended_news_for_user(decode_access_token['email'])

        return user_recommendations

    except CustomQSportException as e:
        logger.error(f"Error in Get Recommendations /: {str(e)}")
        return get_custom_error_response(e)
