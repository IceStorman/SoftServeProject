import requests

from abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class NbaDataManager(AbstractSportDataManager):
    def __init__(self):
        super().__init__()
        self._sport_name = "nba"

    def get_games_statistics(self, api_data: Dict[str, str]) -> Dict[str, str]:
        game_id = api_data.get("game_id")
        if not game_id:
            return {"error": "Missing or invalid parameter: 'game_id' required."}
        index = f"games/statistics?id={game_id}"
        with SessionLocal() as session:
            check = get_all_blob_indexes_from_db(session, index)
            if check:
                result = get_blob_data_for_all_sports(session, check)
                print("\033[32mxui\033[0m")
                return result
        print("\033[31mxui tam plaval\033[0m")
        url = f"https://v2.nba.api-sports.io/games/statistics?id={game_id}"
        host = "v2.nba.api-sports.io"
        try:
            json_data = super().main_request(host, url, index)
            return json_data
        except Exception as e:
            return {"error": str(e)}