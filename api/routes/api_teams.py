from flask import Blueprint, request
from database.session import SessionLocal
from api.routes.scripts import get_error_response
from service.api_logic.teams_logic import get_teams, get_teams_sport
from service.implementation.auto_request_api.logic_request_by_react import basketball_players, rugby_teams_statistics
from api.routes.cache import cache
from api.routes.dto import UniversalResponseDTO
from exept.exeptions import SoftServeException

session = SessionLocal()
teams_app = Blueprint('teams', __name__)


@teams_app.errorhandler(SoftServeException)
def handle_db_timeout_error(e):
    response = e.get_response()
    return response


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
        dto = UniversalResponseDTO(**data)
        cache_key = f"teams:{dto.sport}:{dto.country_id}:{dto.league_id}"

        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data, 200

        all_teams = get_teams_sport(session, dto)
        cache.set(cache_key, all_teams, timeout=60*60)
        return all_teams
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route('/statistics', methods=['POST'])
@cache.cached(timeout=60*1.3)
def get_teams_statistics_endpoint():
    try:
        data = request.get_json()
        dto = UniversalResponseDTO(**data)
        response = rugby_teams_statistics(dto)
        return response
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route('/players', methods=['POST'])
def get_players_endpoint():
    try:
        data = request.get_json()
        dto = UniversalResponseDTO(**data)
        response = basketball_players(dto)
        return response
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


