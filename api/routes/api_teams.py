from flask import Blueprint, request
from service.api_logic.teams_logic import get_teams
from service.implementation.auto_request_api.logic_request_by_react import basketball_players, rugby_teams_statistics
from api.routes.cache import cache
from dto.api_input import TeamsLeagueDTO, TeamsStatisticsOrPlayersDTO
from exept.exeptions import DatabaseConnectionError
from exept.handle_exeptions import get_error_response

teams_app = Blueprint('teams', __name__)


@teams_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    response = {"error in data base": str(e)}
    return response

@teams_app.route("/", methods=['GET'])
def get_teams_endpoint():
    try:
        dto = TeamsLeagueDTO()
        all_teams = get_teams(dto)
        return all_teams
    except Exception as e:
        get_error_response(e)


@teams_app.route("/league", methods=['POST'])
def get_teams_sport_endpoint():
    try:
        data = request.get_json()
        dto = TeamsLeagueDTO(**data)
        league_teams = get_teams(dto)
        return league_teams
    except Exception as e:
        get_error_response(e)


@teams_app.route('/statistics', methods=['POST'])
@cache.cached(timeout=60*1.3)
def get_teams_statistics_endpoint():
    try:
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO(**data)
        team_statistics = rugby_teams_statistics(dto)
        return team_statistics
    except Exception as e:
        get_error_response(e)


@teams_app.route('/players', methods=['POST'])
def get_players_endpoint():
    try:
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO(**data)
        team_players = basketball_players(dto)
        return team_players
    except Exception as e:
        get_error_response(e)



