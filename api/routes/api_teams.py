from flask import Blueprint, request
from database.session import SessionLocal
from api.routes.scripts import get_error_response
from service.api_logic.teams_logic import get_teams
from service.implementation.auto_request_api.logic_request_by_react import basketball_players, rugby_teams_statistics
from api.routes.cache import cache
from dto.api_input import TeamsLeagueDTO, TeamsStatisticsOrPlayersDTO
from exept.exeptions import DatabaseConnectionError
from service.implementation.auto_request_api.sport_data_managers.team_statistics_data_manager import \
    TeamStatisticsDataManager

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
        all_teams = get_teams(session, dto)
        return all_teams
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route("/league", methods=['POST'])
def get_teams_sport_endpoint():
    try:
        data = request.get_json()
        dto = TeamsLeagueDTO(**data)
        league_teams = get_teams(session, dto)
        return league_teams
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route('/statistics', methods=['POST'])
#@cache.cached(timeout=60*1.3)
def get_teams_statistics_endpoint():
    try:
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO(**data)
        data_manager = TeamStatisticsDataManager(dto, dto.sport_id)
        team_statistics = data_manager.get_teams_statistics()
        return team_statistics
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route('/players', methods=['POST'])
def get_players_endpoint():
    try:
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO(**data)
        team_players = basketball_players(dto)
        return team_players
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


