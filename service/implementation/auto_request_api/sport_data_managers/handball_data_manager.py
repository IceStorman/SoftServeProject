import requests

from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class HandballDataManager(AbstractSportDataManager):
    def __init__(self, new_api_data: Dict[str, str]):
        super().__init__(new_api_data)
        self._sport_name = "handball"
        self._host = "v1.handball.api-sports.io"

    def get_teams_statistics(self) -> Dict[str, str]:
        url = f"https://v1.handball.api-sports.io/teams/statistics?season=2024&team={self._team_id}&league={self._league_id}"
        index = f"teams/statistics?season=2024&team={self._team_id}&league={self._league_id}"

        return self.try_return_json_data(url, index)
