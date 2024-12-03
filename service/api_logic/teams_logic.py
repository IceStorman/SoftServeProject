import json
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports

TEAMS_JSON = "teams.json"
TEAM_KEY = "team"
DATA_KEY = "data"
SPORT_KEY = "sport"
RESPONSE_KEY = "response"

def get_teams(session):
    blob_indexes = get_all_blob_indexes_from_db(session, TEAMS_JSON)
    result = get_blob_data_for_all_sports(session, blob_indexes)
    data = json.loads(result)
    filtered_data = []

    for teams_data in data:
        processed_data = process_blob_data(teams_data)
        if processed_data:
            filtered_data.append(processed_data)
    return filtered_data, 200


def process_blob_data(sport_data):
    blob_name = sport_data.get("blob_name")
    team = sport_data.get(DATA_KEY, {}).get(RESPONSE_KEY, [])
    sport = sport_data.get(SPORT_KEY)
    if team:
        return {
            "sport": sport,
            #"blob_name": blob_name,
            TEAM_KEY: team,
        }

    return None