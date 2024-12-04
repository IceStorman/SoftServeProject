from flask import Blueprint, jsonify, request
from database.session import SessionLocal
from api.routes.scripts import get_error_response
from service.api_logic.teams_logic import get_teams

session = SessionLocal()
teams_app = Blueprint('teams', __name__)

@teams_app.errorhandler(Exception)
def handle_exception(e):
    response = {"error in service": str(e)}
    return get_error_response(response, 500)


@teams_app.route("/", methods=['GET'])
def get_teams_endpoint():
    try:
        all_teams = get_teams(session)
        return all_teams
    except Exception as e:
        print(e)
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
        return response
    except Exception as e:
        print(e)


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
        return response
    except Exception as e:
       print(e)

