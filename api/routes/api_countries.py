from flask import Blueprint
from service.api_logic.countries_logic import get_countries, search_countries
from exept.exeptions import DatabaseConnectionError
from exept.handle_exeptions import get_error_response

countries_app = Blueprint('countries_app', __name__)

@countries_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    response = {"error in data base": str(e)}
    return response

@countries_app.route('/', methods=['GET'])
def get_countries_endpoint():
    try:
        countries = get_countries()
        return countries
    except Exception as e:
        get_error_response(e)


@countries_app.route('/search/<query>', methods=['GET'])
def search_countries_endpoint(query):
    try:
        result = search_countries(query.lower())
        return result
    except Exception as e:
        get_error_response(e)


