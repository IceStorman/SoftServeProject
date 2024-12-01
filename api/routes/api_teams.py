from flask import Blueprint, jsonify, request
from database.session import SessionLocal

session = SessionLocal()
teams_app = Blueprint('teams', __name__)

def make_cache_key():
   sport_type = request.view_args.get('sport_type')  # Отримання значення sport_type із запиту
   return f"sport_stream_{sport_type}"


@teams_app.route('/statistics', methods=['POST'])
def get_teams_statistics_endpoint():
    try:
        data = request.get_json()
        sport = data.get("sport", "Unknown")
        team_id = data.get("team_id", "Unknown")
        response = {
            "sport": sport,
            "team_id": team_id,
        }
        #response = teams_statistics_info()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@teams_app.route('/players', methods=['POST'])
def get_players_endpoint():
    try:
        data = request.get_json()
        sport = data.get("sport", "Unknown")
        team_id = data.get("team_id", "Unknown")
        response = {
            "sport": sport,
            "team_id": team_id,
        }
        #response = players_info()
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

