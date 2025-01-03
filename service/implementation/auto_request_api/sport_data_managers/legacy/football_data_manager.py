import requests

from service.implementation.auto_request_api.sport_data_managers.abstract_sport_data_manager import AbstractSportDataManager
from database.azure_blob_storage.save_get_blob import get_all_blob_indexes_from_db, get_blob_data_for_all_sports
from database.session import SessionLocal
from typing import Dict

class FootballDataManager(AbstractSportDataManager):
    _fixture_id: str

    def __init__(self, new_api_data: Dict[str, str]):
        super().__init__(new_api_data)

        self._sport_name = "football"
        self._host = "v3.football.api-sports.io"
        self._fixture_id = self.api_data.get("fixture_id")

    def get_fixtures_statistics(self) -> Dict[str, str]:
        url = f"https://v3.football.api-sports.io/fixtures/statistics?fixture={self._fixture_id}&team={self._team_id}"
        index = f"fixtures/statistics?fixture={self._fixture_id}&team={self._team_id}"

        return self.try_return_json_data(url, index)

    def get_fixtures_events_lineups_players(self) -> Dict[str, Dict[str, str]]:
        events_index = f"fixtures/events?fixture={self._fixture_id}"
        lineups_index = f"fixtures/lineups?fixture={self._fixture_id}"
        players_index = f"fixtures/players?fixture=1300109{self._fixture_id}"
        events_url = f"https://v3.football.api-sports.io/fixtures/events?fixture={self._fixture_id}"
        lineups_url = f"https://v3.football.api-sports.io/fixtures/lineups?fixture={self._fixture_id}"
        players_url = f"https://v3.football.api-sports.io/fixtures/players?fixture={self._fixture_id}"

        return {
            "events": self.try_return_json_data(events_url, events_index),
            "lineups": self.try_return_json_data(lineups_url, lineups_index),
            "players": self.try_return_json_data(players_url, players_index)
        }

    def get_coaches(self) -> Dict[str, str]:
        url = f"https://v3.football.api-sports.io/coachs?team={self._team_id}"
        index = f"coachs/coachs?team={self._team_id}"

        return self.try_return_json_data(url, index)

    def get_players_profiles_sidelined(self) -> Dict[str, Dict[str, str]]:
        profiles_url = f"https://v3.football.api-sports.io/players/profiles?player=276{self._player_id}"
        sidelined_url = f"https://v3.football.api-sports.io/players?id={self._player_id}&season=2024"
        sidelined_players_url = f"https://v3.football.api-sports.io/sidelined?player={self._player_id}"
        profiles_index = f"players/profiles?player={self._player_id}"
        sidelined_index = f"players/players?id={self._player_id}&season=2024"
        sidelined_players_index = f"players/sidelined?player={self._player_id}"

        return {
            "profiles": self.try_return_json_data(profiles_url, profiles_index),
            "sidelined": self.try_return_json_data(sidelined_url, sidelined_index),
            "sidelined_players": self.try_return_json_data(sidelined_players_url, sidelined_players_index)
        }