import json
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from exept.exeptions import SportNotFoundError, DatabaseConnectionError
from exept.colors_text import print_error_message
from api.routes.scripts import get_error_response
from service.api_logic.scripts import get_sport_by_name
from sqlalchemy.exc import OperationalError


TEAMS_JSON = "teams.json"
TEAM_KEY = "team"
DATA_KEY = "data"
SPORT_KEY = "sport"
RESPONSE_KEY = "response"

def get_teams(session):
    try:
        blob_indexes = get_all_blob_indexes_from_db(session, TEAMS_JSON)
        result = get_blob_data_for_all_sports(session, blob_indexes)
        data = json.loads(result)
        filtered_data = []

        for teams_data in data:
            processed_data = process_blob_data(teams_data)
            if processed_data:
                filtered_data.append(processed_data)
        return filtered_data, 200
    except OperationalError:
        raise DatabaseConnectionError()


def process_blob_data(sport_data):
    team = sport_data.get(DATA_KEY, {}).get(RESPONSE_KEY, [])
    sport = sport_data.get(SPORT_KEY)
    if team:
        return {
            SPORT_KEY: sport,
            TEAM_KEY: team,
        }
    return None


def get_teams_sport(session, sport_type):
    try:
        sport = get_sport_by_name(session, sport_type)
    except SportNotFoundError as e:
        print_error_message({"error": e.message})
        return get_error_response({"error": e.message}, 404)
    blob_indexes = get_all_blob_indexes_from_db(session, TEAMS_JSON)
    result = get_blob_data_for_all_sports(session, blob_indexes)
    data = json.loads(result)
    filtered_data = []
    for teams_data in data:
        if sport_type == teams_data.get(SPORT_KEY):
            processed_data = process_blob_data(teams_data)
            if processed_data:
                filtered_data.append(processed_data)
    return filtered_data, 200