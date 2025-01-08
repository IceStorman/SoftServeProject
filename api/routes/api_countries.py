import logging
from flask import Blueprint, request
from service.api_logic.countries_logic import get_countries, search_countries
from exept.exeptions import DatabaseConnectionError
from exept.handle_exeptions import get_error_response
from logger.logger import get_logger, log_function_call

api_routes_logger = get_logger("api_routes_loger", "api_routes.log")

countries_app = Blueprint('countries_app', __name__)

@countries_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    api_routes_logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response

@countries_app.route('/', methods=['GET'])
@log_function_call(api_routes_logger)
def get_countries_endpoint():
    try:
        countries = get_countries()
        return countries
    except Exception as e:
        get_error_response(e)


@countries_app.route('/search/<query>', methods=['GET'])
@log_function_call(api_routes_logger)
def search_countries_endpoint(query):
    try:
        result = search_countries(query.lower())
        return result
    except Exception as e:
        return get_error_response(e)