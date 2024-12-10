import requests

from abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class NbaDataManager(AbstractSportDataManager):
    def __init__(self, new_api_data: Dict[str, str]):
        super().__init__(new_api_data)
        self._sport_name = "nba"
        self._host = "v2.nba.api-sports.io"

    def get_games_statistics(self) -> Dict[str, str]:
        url = f"https://v2.nba.api-sports.io/games/statistics?id={self._game_id}"
        index = f"games/statistics?id={self._game_id}"

        return self.try_return_json_data(url, index)