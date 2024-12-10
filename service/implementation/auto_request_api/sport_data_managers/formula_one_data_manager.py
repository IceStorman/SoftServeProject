import requests

from abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class FormulaOneDataManager(AbstractSportDataManager):
    def __init__(self, new_api_data: Dict[str, str]):
        super().__init__(new_api_data)
        self._sport_name = "formula_one"
        self._host = "v1.formula-1.api-sports.io"

    def get_rankings_races_and_fastestlaps(self) -> Dict[str, Dict[str, str]]:
        races_url = f"https://v1.formula-1.api-sports.io/rankings/races?race={self._race_id}"
        fastest_laps_url = f"https://v1.formula-1.api-sports.io/rankings/fastestlaps?race={self._race_id}"
        races_index = f"rankings/races?race={self._race_id}"
        fastest_laps_index = f"rankings/fastestlaps?race={self._race_id}"

        return {
            "races": self.try_return_json_data(races_url, races_index),
            "fastestlaps": self.try_return_json_data(fastest_laps_url, fastest_laps_index)
        }