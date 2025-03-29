import pytest
from unittest.mock import patch
from database.postgres import save_api_data
from database.postgres.dto import PlayerDTO


class TestPlayersSavingData:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.sport_name = "mma"


    @patch('database.postgres.dal.PlayerDal.save_players')
    def test_parameters_with_team(self, mock_save_players):
        json_case_valid_parameters = {
            "get": "players",
            'parameters': {
                'team': 148
            },
            "response": [{}]
        }

        save_api_data(json_case_valid_parameters, self.sport_name)
        mock_save_players.assert_called_once_with([])

    @patch('database.postgres.dal.PlayerDal.save_players')
    def test_full_info(self, mock_save_players):
        json_case_full_info = {
            "get": "players",
            'parameters': {},
            "response": [
                {
                    "id": 6,
                    "name": "Neymar",
                    "photo": "https://media.api-sports.io/football/players/276.png",
                    "team": [
                        {
                            "id": 4,
                            "name": "SBG Ireland"
                        }
                    ]
                },
                {
                    "id": 3,
                    "name": "John Doe",
                    "photo": "https://example.com/john_doe.png",
                }
            ]
        }

        save_api_data(json_case_full_info, self.sport_name)
        mock_save_players.assert_called_once_with([
            PlayerDTO(
            name="Neymar",
            logo="https://media.api-sports.io/football/players/276.png",
            sport_id=11,
            api_id=6,
            team_index_id=1414
            ),
            PlayerDTO(
                name="John Doe",
                logo="https://example.com/john_doe.png",
                sport_id=11,
                api_id=3,
                team_index_id=None
            )
        ])


    @patch('database.postgres.dal.PlayerDal.save_players')
    def test_full_bad_info(self, mock_save_players):
        json_case_full_bad_info = {
            "get": "players",
            'parameters': {},
            "response": [
                {
                    "player": {
                        "id": 2222,
                        "name": "Neymar",
                        "photo": "https://media.api-sports.io/football/players/276.png",
                        "team": {
                            "id": 40,
                            "name": "SBG Ireland"
                        }
                    }
                },
                {
                    "player": {
                        "id": 3,
                        "name": "John Doe",
                        "photo": "https://example.com/john_doe.png",
                        "team": {
                            "id": 50,
                            "name": "Team Alpha"
                        }
                    }
                }
            ]
        }

        save_api_data(json_case_full_bad_info, self.sport_name)
        mock_save_players.assert_called_once_with([
            PlayerDTO(
                name="Neymar",
                logo="https://media.api-sports.io/football/players/276.png",
                sport_id=11,
                api_id=2222,
                team_index_id=1450
            ),
            PlayerDTO(
                name="John Doe",
                logo="https://example.com/john_doe.png",
                sport_id=11,
                api_id=3,
                team_index_id=1460
            )
        ])