from flask import Blueprint, request
from service.api_logic.sports_logic import get_all_sports, get_all_leagues_by_sport
from database.session import SessionLocal
from api.routes.scripts import get_error_response
from api.routes.cache import cache
from exept.exeptions import DatabaseConnectionError

session = SessionLocal()
sports_app = Blueprint('sports', __name__)


@sports_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    response = {"error in data base": str(e)}
    return get_error_response(response, 503)


@sports_app.route('/all', methods=['GET'])
@cache.cached(timeout=60*60)
def get_all_sports_endpoint():
    try:
        sports = get_all_sports(session)
        return sports
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)

@sports_app.route('/league', methods=['POST'])
@cache.cached(timeout=60*60)
def get_all_leagues_endpoint():
    try:
        data = request.get_json()
        sport_name = data.get("sport", "Unknown")
        page = data.get("page", 1)
        per_page = data.get("per_page", 10)
        sports = get_all_leagues_by_sport(session, sport_name, page, per_page)
        return sports
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)
