import requests

from sport_data import SportData
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class FootballData(SportData):
    _fixture_id: str
    _team_id: str

    def __init__(self):
        super().__init__(self)

        self._sport_name = "football"
        self._fixture_id = self._api_data.get("fixture_id")
        self._team_id = self._api_data.get("team_id")

    def try_to_get_data_from_database(self, index_list: list) -> Dict[str, str]:
        result: Dict[str, str] = {}
        with SessionLocal() as session:
            for index in index_list:
                check = get_all_blob_indexes_from_db(session, index)
                if check:
                    data = get_blob_data_for_all_sports(session, check)
                    result.update({index: data})
                else:
                    return {}

        return result

    def get_team_statistics(self) -> Dict[str, str]:
        super().get_team_statistics()

        if not self._fixture_id or not self._team_id:
            return {"error": "Missing or invalid parameters: 'fixture_id' and 'team_id' are required."}

        index = f"fixtures/statistics?fixture={self._fixture_id}&team={self._team_id}"
        with SessionLocal() as session:
            check = get_all_blob_indexes_from_db(session, index)
            if check:
                result = get_blob_data_for_all_sports(session, check)
                print("\033[32mxui\033[0m")
                return result
        print("\033[31mxui tam plaval\033[0m")
        url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={self._fixture_id}&team={self._team_id}"
        host = "v3.football.api-sports.io"
        try:
            json_data = self.main_request(host, url, index)
            return json_data
        except Exception as e:
            return {"error": str(e)}

    def get_fixtures_events_lineups_players(self) -> Dict[str, Dict[str, str]]:
        if not self._fixture_id:
            return {"error": {"message": "Missing or invalid parameter: 'fixture_id' required."}}

        index1 = f"fixtures/events?fixture={self._fixture_id}"
        index2 = f"fixtures/lineups?fixture={self._fixture_id}"
        index3 = f"fixtures/players?fixture=1300109{self._fixture_id}"

        with SessionLocal() as session:
            check1 = get_all_blob_indexes_from_db(session, index1)
            check2 = get_all_blob_indexes_from_db(session, index2)
            check3 = get_all_blob_indexes_from_db(session, index3)
            if check1 and check2 and check3:
                result1 = get_blob_data_for_all_sports(session, check1)
                result2 = get_blob_data_for_all_sports(session, check2)
                result3 = get_blob_data_for_all_sports(session, check3)
                print("\033[32mxui\033[0m")
                return {
                    "events": result1,
                    "lineups": result2,
                    "players": result3
                }
        print("\033[31mxui tam plaval\033[0m")
        url1 = f"https://v3.football.api-sports.io/fixtures/events?fixture={self._fixture_id}"
        url2 = f"https://v3.football.api-sports.io/fixtures/lineups?fixture={self._fixture_id}"
        url3 = f"https://v3.football.api-sports.io/fixtures/players?fixture={self._fixture_id}"
        host = "v3.football.api-sports.io"
        try:
            json_data1 = self.main_request(host, name, url1, index1)
            json_data2 = self.main_request(host, name, url2, index2)
            json_data3 = self.main_request(host, name, url3, index3)
            return {
                "events": json_data1,
                "lineups": json_data2,
                "players": json_data3
            }
        except Exception as e:
            return {"error": {"message": str(e)}}
