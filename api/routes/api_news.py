from dependency_injector.wiring import Provide, inject
from flask import Blueprint, request, make_response
from api.routes.cache import cache
from api.routes.scripts import get_cache_key
from exept.handle_exeptions import get_custom_error_response, get_exception_error_response
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from dependency_injector.wiring import inject, Provide
from api.container.container import Container
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from logger.logger import Logger
from exept.handle_exeptions import handle_exceptions
from service.api_logic.news_logic import NewsService
from service.api_logic.recommendation_logic import RecommendationService
from dto.api_input import InputUserByIdDTO


logger = Logger("logger", "all.log")

news_app = Blueprint('news', __name__)
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
def get_recent_news_endpoint(service: NewsService = Provide[Container.news_service]):
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
def get_sport_news_endpoint(sport_type, service: NewsService = Provide[Container.news_service]):
    try:
        sport_news = service.get_latest_sport_news(COUNT_NEWS, sport_type)
        return sport_news
    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        get_custom_error_response(e)


@news_app.route('/popular', methods=['GET'])
@cache.cached(timeout=60*3)
@inject
@handle_exceptions
@logger.log_function_call()
def get_popular_news_endpoint(service: NewsService = Provide[Container.news_service]):
    try:
        popular_news = service.get_popular_news(COUNT_NEWS)
        return popular_news
    except CustomQSportException as e:
        logger.error(f"Error in GET /: {str(e)}")
        get_custom_error_response(e)


@news_app.route('/article', methods=['POST'])
@inject
@handle_exceptions
@logger.log_function_call()
def specific_article(service: NewsService = Provide[Container.news_service]):
    try:
        article = request.get_json()
        news_id=article['blob_id']
        response = service.get_news_by_id(news_id)
        return response
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)



@news_app.route("/get/recommendation", methods=["GET"])
@inject
@handle_exceptions
@logger.log_function_call()
async def get_recommendations_endpoint(
        service_recs: RecommendationService = Provide[Container.recommendation_service],
        service_news: NewsService = Provide[Container.news_service],
    ):
    try:
        #user_id = get_user_id_from_jwt()
        user_id = request.cookies.get("snfu")
        rec = await service_recs.get_recommendations_from_db(user_id)
        all_recs_with_data = await service_news.send_all_info_from_blob_to_user(rec)

        return all_recs_with_data

    except CustomQSportException as e:
        logger.error(f"Error in Get Recommendations /: {str(e)}")
        get_custom_error_response(e)


@news_app.route("/fast/recommendation", methods=["POST"])
@inject
@handle_exceptions
@logger.log_function_call()
async def fast_generate_recommendation_endpoint(service_recs: RecommendationService = Provide[Container.recommendation_service]):
    try:
        data = request.get_json()
        dto = InputUserByIdDTO().load(data)
        rec = await service_recs.hybrid_recommendations(dto)
        return rec

    except CustomQSportException as e:
        logger.error(f"Error in Get Recommendations /: {str(e)}")
        return get_custom_error_response(e)

@news_app.route("/qwerty")
def qwerty():
    response = make_response("Hello Nigga")
    response.set_cookie("snfu", "2")
    return response


# def get_user_id_from_jwt():
#     jwt_token = request.cookies.get('access_token')
#     if jwt_token is None:
#         raise Exception("JWT token not found in cookies")
#
#     try:
#         decoded_payload = jwt.decode(
#             jwt_token,
#             current_app.config['JWT_SECRET_KEY'],
#             algorithms=["HS256"]
#         )
#         user_id = decoded_payload['identity']
#         return user_id
#     except jwt.ExpiredSignatureError:
#         raise Exception("JWT token has expired")
#     except jwt.InvalidTokenError:
#         raise Exception("Invalid JWT token")




