import requests
from datetime import datetime
from ..logic_auto_request import current_key_index, token_usage, api_key
from database.azure_blob_storage.save_get_blob import blob_save_specific_api, get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class SportData:
    _sport_name: str
    _api_data: Dict[str, str]

    def __init__(self):
        pass

    def main_request(self, host, url, blob_name):
        global current_key_index, account_url
        today = datetime.now().strftime('%Y-%m-%d')

        if token_usage[SportData._sport_name] >= 99:
            current_key_index = (current_key_index + 1) % len(api_key)
            token_usage[SportData._sport_name] = 0

        token_usage[SportData._sport_name] += 1
        headers = {
            'x-rapidapi-host': host,
            'x-rapidapi-key': api_key[current_key_index]
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        blob_save_specific_api(SportData._sport_name, blob_name, json_data)

        return json_data

    def get_team_statistics(self):
        pass

    def get_player_statistics(self):
        pass

    def get_players(self):
        pass