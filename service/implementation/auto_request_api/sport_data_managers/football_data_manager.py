import requests

from abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class FootballDataManager(AbstractSportDataManager):
    _fixture_id: str
    _team_id: str

    def __init__(self):
        super().__init__()

        self._sport_name = "football"
        self._fixture_id = self._api_data.get("fixture_id")
        self._team_id = self._api_data.get("team_id")

    def get_fixtures_statistics(self, api_data: Dict[str, str]) -> Dict[str, str]:
        fixture_id = api_data.get("fixture_id")
        team_id = api_data.get("team_id")
        if not fixture_id or not team_id:
            return {"error": "Missing or invalid parameters: 'fixture_id' and 'team_id' are required."}
        index = f"fixtures/statistics?fixture={fixture_id}&team={team_id}"
        with SessionLocal() as session:
            check = get_all_blob_indexes_from_db(session, index)
            if check:
                result = get_blob_data_for_all_sports(session, check)
                print("\033[32mxui\033[0m")
                return result
        print("\033[31mxui tam plaval\033[0m")
        url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}&team={team_id}"
        host = "v3.football.api-sports.io"
        try:
            json_data = super().main_request(host, url, index)
            return json_data
        except Exception as e:
            return {"error": str(e)}

    def get_fixtures_events_lineups_players(self, api_data: Dict[str, str]) -> Dict[str, Dict[str, str]]:
        fixture_id = api_data.get("fixture_id")
        if not fixture_id:
            return {"error": {"message": "Missing or invalid parameter: 'fixture_id' required."}}
        index1 = f"fixtures/events?fixture={fixture_id}"
        index2 = f"fixtures/lineups?fixture={fixture_id}"
        index3 = f"fixtures/players?fixture=1300109{fixture_id}"
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
        url1 = f"https://v3.football.api-sports.io/fixtures/events?fixture={fixture_id}"
        url2 = f"https://v3.football.api-sports.io/fixtures/lineups?fixture={fixture_id}"
        url3 = f"https://v3.football.api-sports.io/fixtures/players?fixture={fixture_id}"
        host = "v3.football.api-sports.io"
        try:
            json_data1 = super().main_request(host, url1, index1)
            json_data2 = super().main_request(host, url2, index2)
            json_data3 = super().main_request(host, url3, index3)
            return {
                "events": json_data1,
                "lineups": json_data2,
                "players": json_data3
            }
        except Exception as e:
            return {"error": {"message": str(e)}}

    def get_coaches(self, api_data: Dict[str, str]) -> Dict[str, str]:
        team_id = api_data.get("team_id")
        if not team_id:
            return {"error": "Missing or invalid parameter: 'team_id' required."}
        index = f"coachs/coachs?team={team_id}"
        with SessionLocal() as session:
            check = get_all_blob_indexes_from_db(session, index)
            if check:
                result = get_blob_data_for_all_sports(session, check)
                print("\033[32mxui\033[0m")
                return result
        print("\033[31mxui tam plaval\033[0m")
        url = f"https://v3.football.api-sports.io/coachs?team={team_id}"
        host = "v3.football.api-sports.io"
        try:
            json_data = super().main_request(host, url, index)
            return json_data
        except Exception as e:
            return {"error": str(e)}

    def get_players_profiles_sidelined(self, api_data: Dict[str, str]) -> Dict[str, str]:
        player_id = api_data.get("player_id")
        if not player_id:
            return {"error": "Missing or invalid parameter: 'player_id' required."}
        index1 = f"players/profiles?player={player_id}"
        index2 = f"players/players?id={player_id}&season=2024"
        index3 = f"players/sidelined?player={player_id}"
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
                    "profiles": result1,
                    "players": result2,
                    "sidelined": result3
                }
        print("\033[31mxui tam plaval\033[0m")
        url1 = f"https://v3.football.api-sports.io/players/profiles?player=276{player_id}"
        url2 = f"https://v3.football.api-sports.io/players?id={player_id}&season=2024"
        url3 = f"https://v3.football.api-sports.io/sidelined?player={player_id}"
        host = "v3.football.api-sports.io"
        try:
            json_data1 = super().main_request(host, url1, index1)
            json_data2 = super().main_request(host, url2, index2)
            json_data3 = super().main_request(host, url3, index3)
            return {
                "profiles": json_data1,
                "players": json_data2,
                "sidelined": json_data3
            }
        except Exception as e:
            return {"error": str(e)}