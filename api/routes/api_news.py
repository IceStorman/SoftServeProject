import logging
from flask import Blueprint,request
from service.api_logic.news_logic import get_news_by_count, get_latest_sport_news, get_popular_news, get_news_by_id
from api.routes.cache import cache
from api.routes.scripts import get_cache_key
from exept.handle_exeptions import get_error_response
from exept.exeptions import DatabaseConnectionError

logging.basicConfig(
    filename="appRoute.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
)

news_app = Blueprint('news', __name__)
COUNT_NEWS = 5

@news_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logging.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@news_app.route('/recent', methods=['GET'])
@cache.cached(timeout=60*60)
def get_recent_news_endpoint():
    try:
        logging.info(f"GET request to / from {request.remote_addr}")
        recent_news = get_news_by_count(COUNT_NEWS)
        logging.info(f"Successfully retrieved recent_news.")
        return recent_news
    except Exception as e:
        logging.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@news_app.route('/<sport_type>', methods=['GET'])
@cache.cached(timeout=60*60, key_prefix=get_cache_key)
def get_sport_news_endpoint(sport_type):
    try:
        logging.info(f"GET request to / from {request.remote_addr}")
        sport_news = get_latest_sport_news(COUNT_NEWS, sport_type)
        logging.info(f"Successfully retrieved sport_news.")
        return sport_news
    except Exception as e:
        logging.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@news_app.route('/popular', methods=['GET'])
@cache.cached(timeout=60*3)
def get_popular_news_endpoint():
    try:
        logging.info(f"GET request to / from {request.remote_addr}")
        popular_news = get_popular_news(COUNT_NEWS)
        logging.info(f"Successfully retrieved popular_news.")
        return popular_news
    except Exception as e:
        logging.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@news_app.route('/article', methods=['POST'])
def specific_article():

    try:
        logging.info(f"GET request to / from {request.remote_addr}")
        article = request.get_json()
        news_id=article['blob_id']
        response = get_news_by_id(news_id)
        logging.info(f"Successfully retrieved response.")
        return response
    except Exception as e:
        logging.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


    




