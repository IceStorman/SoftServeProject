from flask import Blueprint, request, jsonify
from database.session import SessionLocal
from api.routes.scripts import get_error_response, post_cache_key
from service.api_logic.teams_logic import get_teams, get_teams_sport
from api.routes.cache import cache
from api.routes.dto import TeamsLeagueDTO, TeamsStatisticsOrPlayersDTO
from exept.exeptions import DatabaseConnectionError
from service.implementation.auto_request_api.sport_data_managers.sport_facade_data_manager import SportFacadeDataManager

session = SessionLocal()
teams_app = Blueprint('teams', __name__)


@teams_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    response = {"error in data base": str(e)}
    return get_error_response(response, 503)


@teams_app.route("/", methods=['GET'])
def get_teams_endpoint():
    try:
        dto = TeamsLeagueDTO()
        all_teams = get_teams(session, 9, dto)
        response_data = [team.dict() for team in all_teams]

        return jsonify(response_data), 200
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route("/league", methods=['POST'])
def get_teams_sport_endpoint():
    try:
        data = request.get_json()
        dto = TeamsLeagueDTO(**data)
        all_teams = get_teams(session, 9, dto)
        response_data = [team.dict() for team in all_teams]

        return jsonify(response_data), 200
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route('/statistics', methods=['POST'])
@cache.cached(timeout=60*1.3, key_prefix=post_cache_key)
def get_teams_statistics_endpoint():
    try:
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO(**data)
        data_manager = SportFacadeDataManager.get_data_manager(dto.sport, dto)
        response = data_manager.get_teams_statistics() or get_error_response("Null", 404)

        return response
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route('/players', methods=['POST'])
@cache.cached(timeout=60*1.3, key_prefix=post_cache_key)
def get_players_endpoint():
    try:
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO(**data)
        data_manager = SportFacadeDataManager.get_data_manager(dto.sport, dto)
        response = data_manager.get_players() or get_error_response("Null", 404)

        return response
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


