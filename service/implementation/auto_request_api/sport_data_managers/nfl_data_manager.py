import requests

from abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class NflDataManager(AbstractSportDataManager):
    def __init__(self):
        super().__init__()
        self._sport_name = "nfl"

    def get_injuries_players(self, api_data: Dict[str, str]) -> Dict[str, str]:
        team_id = api_data.get("team_id")
        if not team_id:
            return {"error": "Missing or invalid parameter: 'team_id' required."}
        index1 = f"injuries/injuries?team={team_id}"
        index2 = f"players/players?team={team_id}"
        with SessionLocal() as session:
            check1 = get_all_blob_indexes_from_db(session, index1)
            check2 = get_all_blob_indexes_from_db(session, index2)
            if check1 and check2:
                result1 = get_blob_data_for_all_sports(session, check1)
                result2 = get_blob_data_for_all_sports(session, check2)
                print("\033[32mxui\033[0m")
                return {
                    "injuries": result1,
                    "players": result2,
                }
        print("\033[31mxui tam plaval\033[0m")
        url1 = f"https://v1.american-football.api-sports.io/injuries?team={team_id}"
        url2 = f"https://v1.american-football.api-sports.io/players?team={team_id}"
        host = "v1.american-football.api-sports.io"
        try:
            json_data1 = super().main_request(host, url1, index1)
            json_data2 = super().main_request(host, url2, index2)
            return {
                "injuries": json_data1,
                "players": json_data2,
            }
        except Exception as e:
            return {"error": str(e)}