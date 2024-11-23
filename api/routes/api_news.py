from flask import Blueprint, jsonify
from service.api_logic.news_logic import get_news_by_count
from database.session import SessionLocal

session = SessionLocal()
news_app = Blueprint('news', __name__)

@news_app.route('/recent', methods=['GET'])
def get_recent_news_endpoint():
    try:
        recent_news = get_news_by_count(5, session)
        return recent_news, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@news_app.route('/sport/<sport_id>', methods=['GET'])
def test():
    pass