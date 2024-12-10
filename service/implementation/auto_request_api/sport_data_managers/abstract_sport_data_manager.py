import requests
from datetime import datetime
from ..logic_auto_request import current_key_index, token_usage, api_key
from database.azure_blob_storage.save_get_blob import blob_save_specific_api, get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class AbstractSportDataManager:
    api_data: Dict[str, str]

    _sport_name: str
    _host: str

    _api_data: Dict[str, str]
    _team_id: str
    _player_id: str
    _league_id: str
    _game_id: str
    _race_id: str

    def __init__(self, new_api_data: Dict[str, str]):
        self.api_data = new_api_data

        self._team_id = self.api_data.get("team_id")
        if not self._team_id:
            print("error: Missing or invalid parameter: 'team_id' required.")

        self._player_id = self.api_data.get("player_id")
        if not self._player_id:
            print("error: Missing or invalid parameter: 'player_id' required.")

        self._league_id = self.api_data.get("league_id")
        if not self._league_id:
            print("error: Missing or invalid parameter: 'league_id' required.")

        self._game_id = self.api_data.get("game_id")
        if not self._game_id:
            print("error: Missing or invalid parameter: 'game_id' required.")

        self._race_id = self.api_data.get("race_id")
        if not self._race_id:
            print("error: Missing or invalid parameter: 'race_id' required.")


    def main_request(self, host, url, blob_name) -> Dict[str, str]:
        global current_key_index, account_url

        if token_usage[AbstractSportDataManager._sport_name] >= 99:
            current_key_index = (current_key_index + 1) % len(api_key)
            token_usage[AbstractSportDataManager._sport_name] = 0

        token_usage[AbstractSportDataManager._sport_name] += 1
        headers = {
            'x-rapidapi-host': host,
            'x-rapidapi-key': api_key[current_key_index]
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        blob_save_specific_api(AbstractSportDataManager._sport_name, blob_name, json_data)

        return json_data

    def get_players(self) -> Dict[str, str]:
        pass

    def try_return_json_data(self, url: str, index: str) -> Dict[str, str]:
        with SessionLocal() as session:
            check = get_all_blob_indexes_from_db(session, index)
            if check:
                result = get_blob_data_for_all_sports(session, check)
                print("\033[32mxui\033[0m")
                return result
        print("\033[31mxui tam plaval\033[0m")
        try:
            json_data = self.main_request(self._host, url, index)
            return json_data
        except Exception as e:
            return {"error": str(e)}
