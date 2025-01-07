import logging
from flask import Blueprint, request
from service.api_logic.countries_logic import get_countries, search_countries
from exept.exeptions import DatabaseConnectionError
from exept.handle_exeptions import get_error_response

logging.basicConfig(
    filename="appRoute.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"
)

countries_app = Blueprint('countries_app', __name__)

@countries_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logging.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response

@countries_app.route('/', methods=['GET'])
def get_countries_endpoint():
    try:
        logging.info(f"GET request to / from {request.remote_addr}")
        countries = get_countries()
        logging.info(f"Successfully retrieved countries.")
        return countries
    except Exception as e:
        logging.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@countries_app.route('/search/<query>', methods=['GET'])
def search_countries_endpoint(query):
    try:
        logging.info(f"GET request to /search/{query} from {request.remote_addr}")
        result = search_countries(query.lower())
        logging.info(f"Search for '{query}' returned results.")
        return result
    except Exception as e:
        logging.error(f"Error in GET /search/{query}: {str(e)}")
        return get_error_response(e)


