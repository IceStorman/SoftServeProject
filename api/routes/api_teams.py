from flask import Blueprint, request, jsonify
from database.session import SessionLocal
from api.routes.scripts import get_error_response
from service.api_logic.teams_logic import get_teams, fetch_teams
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
def get_teams_endpoint():
    try:
        dto = TeamsLeagueDTO()
        all_teams = fetch_teams(session, dto)
        return all_teams
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route("/league", methods=['POST'])
def get_teams_sport_endpoint():
    try:
        data = request.get_json()
        dto = TeamsLeagueDTO(**data)
        league_teams = fetch_teams(session, dto)
        return league_teams
    except Exception as e:
        response = {"error in service": str(e)}
        return get_error_response(response, 500)


@teams_app.route('/statistics', methods=['POST'])
@cache.cached(timeout=60*1.3)
def get_teams_statistics_endpoint():
    try:
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO(**data)
        team_statistics = rugby_teams_statistics(dto)
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


