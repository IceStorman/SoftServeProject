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

        #TODO: rewrite from dicts to dtos
        self._team_id = self.api_data.get("team_id")
        self._player_id = self.api_data.get("player_id")
        self._league_id = self.api_data.get("league_id")
        self._game_id = self.api_data.get("game_id")
        self._race_id = self.api_data.get("race_id")

    def main_request(self, host, url, blob_name) -> Dict[str, str]:
        global current_key_index, account_url

        if token_usage[self._sport_name] >= 99:
            current_key_index = (current_key_index + 1) % len(api_key)
            token_usage[self._sport_name] = 0

        token_usage[self._sport_name] += 1
        headers = {
            'x-rapidapi-host': host,
            'x-rapidapi-key': api_key[current_key_index]
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        blob_save_specific_api(self._sport_name, blob_name, json_data)

        return json_data

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

    def get_rankings_races_and_fastestlaps(self) -> Dict[str, Dict[str, str]]:
        pass

    def get_injuries_players(self) -> Dict[str, Dict[str, str]]:
        pass

    def get_teams_statistics(self) -> Dict[str, str]:
        pass

    def get_players(self) -> Dict[str, str]:
        pass

    def get_player_statistics(self) -> Dict[str, str]:
        pass

    def get_coaches(self) -> Dict[str, str]:
        pass

    def get_fixtures_statistics(self) -> Dict[str, str]:
        pass

    def get_fixtures_events_lineups_players(self) -> Dict[str, Dict[str, str]]:
        pass

    def get_players_profiles_sidelined(self) -> Dict[str, Dict[str, str]]:
        pass

    def get_games_events(self) -> Dict[str, str]:
        pass

    def get_fighters_records(self) -> Dict[str, str]:
        pass

    def get_games_statistics(self) -> Dict[str, str]:
        pass
