import requests

from abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class BasketballDataManager(AbstractSportDataManager):
    def __init__(self, new_api_data: Dict[str, str]):
        super().__init__(new_api_data)
        self._sport_name = "basketball"
        self._host = "v1.basketball.api-sports.io"

    def get_players(self) -> Dict[str, str]:
        url = f"https://v1.basketball.api-sports.io/players?team={self._team_id}&season=2024"
        index = f"players/players?team={self._team_id}&season=2024"

        return self.try_return_json_data(url, index)

    def get_player_statistics(self) -> Dict[str, str]:
        url = f"https://v1.basketball.api-sports.io/games/statistics/players?id={self._player_id}"
        index = f"players/games/statistics/players?id={self._player_id}"

        return self.try_return_json_data(url, index)