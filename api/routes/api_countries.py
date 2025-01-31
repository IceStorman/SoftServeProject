import logging
from flask import Blueprint, request
from service.api_logic.countries_logic import get_countries, search_countries
from exept.exeptions import DatabaseConnectionError, SoftServeException
from exept.handle_exeptions import get_custom_error_response
from logger.logger import Logger

api_routes_logger = Logger("api_routes_logger", "api_routes_logger.log")

countries_app = Blueprint('countries_app', __name__)

@countries_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    api_routes_logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response

@countries_app.route('/', methods=['GET'])
@api_routes_logger.log_function_call()
def get_countries_endpoint():
    try:
        countries = get_countries()
        return countries
    except SoftServeException as e:
        api_routes_logger.error(f"Error in GET /: {str(e)}")
        get_custom_error_response(e)


@countries_app.route('/search/<query>', methods=['GET'])
@api_routes_logger.log_function_call()
def search_countries_endpoint(query):
    try:
        result = search_countries(query.lower())
        return result
    except SoftServeException as e:
        api_routes_logger.error(f"Error in GET /: {str(e)}")
        get_custom_error_response(e)