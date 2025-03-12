from flask import Blueprint, request
from dto.pagination import Pagination
from exept.handle_exeptions import get_custom_error_response
from service.api_logic.teams_logic import get_teams
from service.implementation.auto_request_api.logic_request_by_react import basketball_players
from api.routes.cache import cache
from dto.api_input import TeamsLeagueDTO, TeamsStatisticsOrPlayersDTO
from exept.exeptions import DatabaseConnectionError, CustomQSportException
from service.implementation.auto_request_api.sport_data_managers.players_data_manager import PlayersDataManager
from service.implementation.auto_request_api.sport_data_managers.team_statistics_data_manager import \
    TeamStatisticsDataManager
from logger.logger import Logger
from service.implementation.auto_request_api.sport_data_managers.teams_data_manager import TeamsDataManager

logger = Logger("logger", "all.log")



CACHE_TEAMS = 60*1.3
teams_app = Blueprint('teams', __name__)


@teams_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logger.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}

    return response


@teams_app.route("/league", methods=['POST'])
@logger.log_function_call()
def get_teams_sport_endpoint():
    try:
        data = request.get_json()
        dto = TeamsLeagueDTO().load(data)
        pagination = Pagination(**data)

        data_manager = TeamsDataManager(dto)
        league_teams = data_manager.get_teams_data(pagination)

        return league_teams
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)


@teams_app.route('/statistics', methods=['POST'])
@logger.log_function_call()
def get_teams_statistics_endpoint():
    try:
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO().load(data)

        data_manager = TeamStatisticsDataManager(dto)
        team_statistics = data_manager.get_teams_statistics()

        return team_statistics
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)


@teams_app.route('/players', methods=['POST'])
@logger.log_function_call()
def get_players_endpoint():
    try:
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO().load(data)

        data_manager = PlayersDataManager(dto)
        team_players = data_manager.get_data()

        return team_players
    except CustomQSportException as e:
        logger.error(f"Error in POST /: {str(e)}")
        get_custom_error_response(e)

