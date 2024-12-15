import json
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from service.api_logic.scripts import get_sport_by_name
from api.routes.dto import UniversalResponseDTO
from exept.handle_exeptions import code_status
from database.models import TeamIndex, Sport
from flask import Response


TEAMS_JSON = "teams.json"
TEAM_KEY = "team"
DATA_KEY = "data"
SPORT_KEY = "sport"
RESPONSE_KEY = "response"


@code_status
def get_teams(session):
    teams_blob_indexes = get_all_blob_indexes_from_db(session, TEAMS_JSON)
    sport_result = get_blob_data_for_all_sports(session, teams_blob_indexes)
    sport_result_json = json.loads(sport_result)
    filtered_data = [
        processed_data
        for teams_data in sport_result_json
        if (processed_data := process_blob_data(teams_data))
    ]
    return filtered_data



@code_status
def process_blob_data(sport_data):
    team = sport_data.get(DATA_KEY, {}).get(RESPONSE_KEY, [])
    sport = sport_data.get(SPORT_KEY)
    if team:
        return {
            SPORT_KEY: sport,
            TEAM_KEY: team,
        }
    return None

@code_status
def get_teams_sport(session, dto: UniversalResponseDTO):

        sport = get_sport_by_name(session, dto.sport)

        teams_by_sport_blob_indexes = get_all_blob_indexes_from_db(session, TEAMS_JSON)
        result = get_blob_data_for_all_sports(session, teams_by_sport_blob_indexes)
        data = json.loads(result)

        filtered_data = [
            processed_data
            for teams_data in data
            if dto.sport == teams_data.get(SPORT_KEY) and (processed_data := process_blob_data(teams_data))
        ]
        return filtered_data




