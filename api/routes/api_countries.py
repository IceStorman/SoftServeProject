from flask import Blueprint, request
from service.api_logic.countries_logic import get_countries
from database.session import SessionLocal
from api.routes.scripts import get_error_response
from exept.exeptions import DatabaseConnectionError

session = SessionLocal()
countries_app = Blueprint('countries_app', __name__)


@countries_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    response = {"error in data base": str(e)}
    return get_error_response(response, 503)


@countries_app.route('/', methods=['GET'])
def get_countries_endpoint():
    try:
        countries = get_countries(session)
        return countries
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@countries_app.route('/search', methods=['GET'])
def search_countries():
    try:
        query = request.args.get('q', '').lower()
        result = search_countries(session, query)
        return result
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)

