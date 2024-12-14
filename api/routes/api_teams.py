from flask import Blueprint, request, jsonify
from database.session import SessionLocal
from api.routes.scripts import get_error_response
from service.api_logic.teams_logic import get_teams, get_teams_sport
from service.implementation.auto_request_api.logic_request_by_react import basketball_players, rugby_teams_statistics
from api.routes.cache import cache
from api.routes.dto import TeamsLeagueDTO, TeamsStatisticsOrPlayersDTO
from exept.exeptions import DatabaseConnectionError

session = SessionLocal()
teams_app = Blueprint('teams', __name__)


@teams_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    response = {"error in data base": str(e)}
    return get_error_response(response, 503)


@teams_app.route("/", methods=['GET'])
@cache.cached(timeout=60*60)
def get_teams_endpoint():
    try:
        all_teams = get_teams(session)
        return all_teams
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route("/league", methods=['POST'])
def get_teams_sport_endpoint():
    try:
        data = request.get_json()
        dto = TeamsLeagueDTO(**data)
        cache_key = f"teams:{dto.sport}:{dto.country_id}:{dto.league_id}"
        print(f"Cache key: {cache_key}")

        cached_data = cache.get(cache_key)
        print(f"Cache hit: {bool(cached_data)}")

        if cached_data:
            return jsonify(cached_data), 200

        all_teams = get_teams(session, dto)
        cache.set(cache_key, all_teams, timeout=60*60)
        response_data = [team.dict() for team in all_teams]
        return jsonify(response_data), 200
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route('/statistics', methods=['POST'])
@cache.cached(timeout=60*1.3)
def get_teams_statistics_endpoint():
    try:
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO(**data)
        response = rugby_teams_statistics(dto)
        return response
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route('/players', methods=['POST'])
def get_players_endpoint():
    try:
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO(**data)
        response = basketball_players(dto)
        return response
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


