import logging
from flask import Blueprint, request
from dto.pagination import Pagination
from exept.handle_exeptions import get_error_response
from service.api_logic.teams_logic import get_teams
from service.implementation.auto_request_api.logic_request_by_react import basketball_players, rugby_teams_statistics
from api.routes.cache import cache
from dto.api_input import TeamsLeagueDTO, TeamsStatisticsOrPlayersDTO
from exept.exeptions import DatabaseConnectionError
from service.implementation.auto_request_api.sport_data_managers.team_statistics_data_manager import \
    TeamStatisticsDataManager
from api.routes.api_routes_logging import setup_logger

setup_logger()

CACHE_TEAMS = 60*1.3
teams_app = Blueprint('teams', __name__)


@teams_app.errorhandler(DatabaseConnectionError)
def handle_db_timeout_error(e):
    logging.error(f"Database error: {str(e)}")
    response = {"error in data base": str(e)}
    return response


@teams_app.route("/league", methods=['POST'])
def get_teams_sport_endpoint():
    try:
        logging.info(f"GET request to / from {request.remote_addr}")
        data = request.get_json()
        dto = TeamsLeagueDTO().load(data)
        pagination = Pagination(**data)
        league_teams = get_teams(dto, pagination)
        logging.info(f"Successfully retrieved league_teams.")
        return league_teams
    except Exception as e:
        logging.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@teams_app.route('/statistics', methods=['POST'])
@cache.cached(timeout=CACHE_TEAMS)
def get_teams_statistics_endpoint():
    try:
        logging.info(f"GET request to / from {request.remote_addr}")
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO().load(data)
        data_manager = TeamStatisticsDataManager(dto, dto.sport_id)
        team_statistics = data_manager.get_teams_statistics()
        logging.info(f"Successfully retrieved team_statistics.")
        return team_statistics
    except Exception as e:
        logging.error(f"Error in GET /: {str(e)}")
        get_error_response(e)


@teams_app.route('/players', methods=['POST'])
def get_players_endpoint():
    try:
        logging.info(f"GET request to / from {request.remote_addr}")
        data = request.get_json()
        dto = TeamsStatisticsOrPlayersDTO(**data)
        team_players = basketball_players(dto)
        logging.info(f"Successfully retrieved team_players.")
        return team_players
    except Exception as e:
        logging.error(f"Error in GET /: {str(e)}")
        get_error_response(e)



