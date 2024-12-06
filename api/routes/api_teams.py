from flask import Blueprint, jsonify, request
from database.session import SessionLocal
from api.routes.scripts import get_error_response
from service.api_logic.teams_logic import get_teams, get_teams_sport
from service.implementation.auto_request_api.logic_request_by_react import basketball_players, rugby_teams_statistics
from api.routes.cache import cache
from exept.exeptions import DatabaseConnectionError
from pyodbc import OperationalError

session = SessionLocal()
teams_app = Blueprint('teams', __name__)

@teams_app.errorhandler(Exception)
def handle_exception(e):
    if isinstance(e, DatabaseConnectionError):
        response = {"error": e.message}
        return get_error_response(response, 503)  # 503 - Service Unavailable
    # Для інших помилок
    response = {"error": "An unexpected error occurred."}
    return get_error_response(response, 500)


@teams_app.errorhandler(OperationalError)
def handle_db_timeout_error(e):
    response = {
        "error": "Database connection timed out. Please try again later.",
        "details": str(e)
    }
    return get_error_response(response, 503)


@teams_app.route("/", methods=['GET'])
@cache.cached(timeout=60*60)
def get_teams_endpoint():
    try:
        all_teams = get_teams(session)
        return all_teams
    except Exception as e:
        print(e)
    except OperationalError as e:
        return handle_db_timeout_error(e)


@teams_app.route("/<sport_type>", methods=['GET'])
@cache.cached(timeout=60*60)
def get_teams_sport_endpoint(sport_type):
    try:
        all_teams = get_teams_sport(session, sport_type)
        return all_teams
    except Exception as e:
        print(e)


@teams_app.route('/statistics', methods=['POST'])
@cache.cached(timeout=60*1.3)
def get_teams_statistics_endpoint():
    try:
        data = request.get_json()
        response = {
            "sport": data.get("sport", "Unknown"),
            "team_id": data.get("team_id", "Unknown"),
            "league_id": 3
        }
        response = rugby_teams_statistics(response)
        return response
    except Exception as e:
        print(e)


@teams_app.route('/players', methods=['POST'])
def get_players_endpoint():
    try:
        data = request.get_json()
        response = {
            "sport": data.get("sport", "Unknown"),
            "team_id": data.get("team_id", "Unknown"),
        }
        response = basketball_players(response)
        return response
    except Exception as e:
       print(e)

