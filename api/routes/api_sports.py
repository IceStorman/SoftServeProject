from flask import Blueprint
from service.api_logic.sports_logic import get_all_sports#, get_all_leagues_by_sport
from database.session import SessionLocal
from api.routes.scripts import get_error_response
from api.routes.cache import cache

session = SessionLocal()
sports_app = Blueprint('sports', __name__)

@sports_app.errorhandler(Exception)
def handle_exception(e):
    response = {"error in service": str(e)}
    return get_error_response(response, 500)


@sports_app.route('/all', methods=['GET'])
@cache.cached(timeout=60*60)
def get_all_sports_endpoint():
    sports = get_all_sports(session)
    return sports

@sports_app.route('/league/<sport_type>', methods=['GET'])
@cache.cached(timeout=60*60)
def get_all_sports_endpoint():
    sports = 1#get_all_leagues_by_sport(session)
    return sports
