from flask import Blueprint, jsonify
from service.api_logic.sports_logic import get_all_sports
from database.session import SessionLocal

session = SessionLocal()
sports_app = Blueprint('sports', __name__)

@sports_app.route('/all', methods=['GET'])
def get_all_sports_endpoint():
    try:
        sports = get_all_sports()
        print(sports)
        return sports, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500