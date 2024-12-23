import requests

from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class NflDataManager(AbstractSportDataManager):
    def __init__(self, new_api_data: Dict[str, str]):
        super().__init__(new_api_data)
        self._sport_name = "nfl"
        self._host = "v1.american-football.api-sports.io"

    def get_injuries_players(self) -> Dict[str, Dict[str, str]]:
        injuries_url = f"https://v1.american-football.api-sports.io/injuries?team={self._team_id}"
        player_url = f"https://v1.american-football.api-sports.io/players?team={self._team_id}"
        injuries_index = f"injuries/injuries?team={self._team_id}"
        player_index = f"players/players?team={self._team_id}"

        return {
            "injuries": self.try_return_json_data(injuries_url, injuries_index),
            "players": self.try_return_json_data(player_url, player_index)
        }