import requests

from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class AflDataManager(AbstractSportDataManager):
    def __init__(self, new_api_data: Dict[str, str]):
        super().__init__(new_api_data)
        self._sport_name = "afl"
        self._host = "v1.afl.api-sports.io"

    def get_teams_statistics(self) -> Dict[str, str]:
        url = f"https://v1.afl.api-sports.io/teams/statistics?id={self._team_id}&season=2023"
        index = f"teams/statistics?id={self._team_id}&season=2023"

        return self.try_return_json_data(url, index)

    def get_players(self) -> Dict[str, str]:
        url = f"https://v1.afl.api-sports.io/players?season=2023&team={self._team_id}"
        index = f"teams/players?season=2023&team={self._team_id}"

        return self.try_return_json_data(url, index)

    def get_player_statistics(self) -> Dict[str, str]:
        url = f"https://v1.afl.api-sports.io/players/statistics?id={self._player_id}&season=2024"
        index = f"players/statistics?id={self._player_id}&season=2024"

        return self.try_return_json_data(url, index)