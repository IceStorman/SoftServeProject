from flask import Blueprint
from service.api_logic.sports_logic import get_all_sports
from database.session import SessionLocal
from api.routes.scripts import get_error_response

session = SessionLocal()
sports_app = Blueprint('sports', __name__)

@sports_app.route('/all', methods=['GET'])
def get_all_sports_endpoint():
    try:
        sports = get_all_sports()
        return sports, 200
    except Exception as e:
        return get_error_response(e), 500