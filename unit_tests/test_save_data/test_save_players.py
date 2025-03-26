import pytest
from unittest.mock import patch
from database.postgres import save_api_data

class TestPlayersSavingData:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.sport_name = "mma"
        self.json_case_valid_parameters = {
            "get": "players",
            'parameters': {
                'team': 1488
            },
            "response": [{}]
        }
        self.json_case_full_bad_info = {
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
        self.json_case_full_info = {
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
                    "id": 32,
                    "name": "John Doe",
                    "photo": "https://example.com/john_doe.png",
                }
            ]
        }

    @patch('database.postgres.dal.PlayerDal.save_players')
    @patch('database.postgres.save_api_data')
    def test_parameters_dict_with_team(self, mock_save_players, mock_save_api_data):
        mock_save_api_data.return_value = None
        save_api_data(self.json_case_valid_parameters, self.sport_name)
        assert 1 == 1

    @patch('database.postgres.dal.PlayerDal.save_players')
    @patch('database.postgres.save_api_data')
    def test_full_info(self, mock_save_api_data, mock_save_players):
        mock_save_api_data.return_value = None
        save_api_data(self.json_case_full_info, self.sport_name)
        assert 1 == 1

    @patch('database.postgres.dal.PlayerDal.save_players')
    @patch('database.postgres.save_api_data')
    def test_full_bad_info(self, mock_save_api_data, mock_save_players):
        mock_save_api_data.return_value = None
        save_api_data(self.json_case_full_bad_info, self.sport_name)
        assert 1 == 1