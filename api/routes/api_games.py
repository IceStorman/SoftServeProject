from flask import Blueprint, jsonify
from service.api_logic.games_logic import get_games_today
from database.session import SessionLocal

session = SessionLocal()
games_app = Blueprint('games_app', __name__)

@games_app.route('/', methods=['GET'])
def get_games_today_endpoint():
   try:
      games = get_games_today(session)
      return games, 200
   except Exception as e:
      return jsonify({"error": str(e)}), 500