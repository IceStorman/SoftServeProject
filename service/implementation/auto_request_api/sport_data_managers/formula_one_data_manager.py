import requests

from abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class FormulaOneDataManager(AbstractSportDataManager):
    def __init__(self):
        super().__init__()
        self._sport_name = "formula_one"

    def get_rankings_races_and_fastestlaps(self, api_data: Dict[str, str]) -> Dict[str, str]:
        race_id = api_data.get("race_id")
        if not race_id:
            return {"error": "Missing or invalid parameter: 'race_id' required."}
        index1 = f"rankings/races?race={race_id}"
        index2 = f"rankings/fastestlaps?race={race_id}"
        with SessionLocal() as session:
            check1 = get_all_blob_indexes_from_db(session, index1)
            check2 = get_all_blob_indexes_from_db(session, index2)
            if check1 and check2:
                result1 = get_blob_data_for_all_sports(session, check1)
                result2 = get_blob_data_for_all_sports(session, check2)
                print("\033[32mxui\033[0m")
                return {
                    "races": result1,
                    "fastestlaps": result2,
                }
        print("\033[31mxui tam plaval\033[0m")
        url1 = f"https://v1.formula-1.api-sports.io/rankings/races?race={race_id}"
        url2 = f"https://v1.formula-1.api-sports.io/rankings/fastestlaps?race={race_id}"
        host = "v1.formula-1.api-sports.io"
        try:
            json_data1 = super().main_request(host, url1, index1)
            json_data2 = super().main_request(host, url2, index2)
            return {
                "races": json_data1,
                "fastestlaps": json_data2,
            }
        except Exception as e:
            return {"error": str(e)}