from flask import Blueprint, request
from database.session import SessionLocal
from api.routes.scripts import get_error_response
from service.api_logic.teams_logic import get_teams, get_teams_sport
from service.implementation.auto_request_api.logic_request_by_react import basketball_players, rugby_teams_statistics
from api.routes.cache import cache
from exept.exeptions import DatabaseConnectionError

session = SessionLocal()
teams_app = Blueprint('teams', __name__)

@teams_app.errorhandler(Exception)
def handle_exception(e):
    response = {"error in service": str(e)}
    return get_error_response(response, 500)


@teams_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    response = {"error in data base": str(e)}
    return get_error_response(response, 503)


@teams_app.route("/", methods=['GET'])
@cache.cached(timeout=60*60)
def get_teams_endpoint():
    all_teams = get_teams(session)
    return all_teams


@teams_app.route("/league/teams", methods=['POST'])
#@cache.cached(timeout=60*60, query_string=True)
def get_teams_sport_endpoint():
    data = request.get_json()
    response = {
        "sport": data.get("sport", "Unknown"),
        "country_id": data.get("country_id", "Unknown"),
        "league_id": data.get("league_id", "Unknown"),
    }
    cache_key = f"teams:{response['sport']}:{response['country_id']}:{response['league_id']}"

    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data, 200

    all_teams = get_teams_sport(session, response)
    cache.set(cache_key, all_teams, timeout=60 * 60)
    return all_teams


@teams_app.route('/statistics', methods=['POST'])
@cache.cached(timeout=60*1.3)
def get_teams_statistics_endpoint():
    data = request.get_json()
    response = {
        "sport": data.get("sport", "Unknown"),
        "team_id": data.get("team_id", "Unknown"),
        "league_id": 3
    }
    response = rugby_teams_statistics(response)
    return response


@teams_app.route('/players', methods=['POST'])
def get_players_endpoint():
    data = request.get_json()
    response = {
        "sport": data.get("sport", "Unknown"),
        "team_id": data.get("team_id", "Unknown"),
    }
    response = basketball_players(response)
    return response


