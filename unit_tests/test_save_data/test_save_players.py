import pytest
from database.postgres import save_api_data

class TestPlayersSavingData:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.sport_name = "mma"
        self.json_case_empty = {}
        self.json_case_empty_parameters = {
            "get": "players",
            'parameters': {},
            "response": {
                "player": {
                    "id": 276,
                    "name": "Neymar",
                    "photo": "https://media.api-sports.io/football/players/276.png"
                }
            }
        }
        self.json_case_valid_parameters = {
            "get": "players",
            'parameters': {
                'team': 1488
            }
        }
        self.json_case_full_bad_info = {
            "get": "players",
            'parameters': {},
            "response": [
                {
                    "player": {
                        "id": 276,
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
                        "id": 301,
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
                    "id": 276,
                    "name": "Neymar",
                    "photo": "https://media.api-sports.io/football/players/276.png",
                    "team": [
                        {
                            "id": 40,
                            "name": "SBG Ireland"
                        }
                    ]
                },
                {
                    "id": 302,
                    "name": "John Doe",
                    "photo": "https://example.com/john_doe.png",
                    "team": [
                        {
                            "id": 55,
                            "name": "Beta Warriors"
                        }
                    ]
                }
            ]
        }

    def test_parameters_missing(self):
        save_api_data(self.json_case_empty, self.sport_name)
        assert 1 == 1

    def test_parameters_empty_list(self):
        save_api_data(self.json_case_empty_parameters, self.sport_name)
        assert 1 == 1

    def test_parameters_dict_with_team(self):
        save_api_data(self.json_case_valid_parameters, self.sport_name)
        assert 1 == 1

    def test_full_info(self):
        save_api_data(self.json_case_full_info, self.sport_name)
        assert 1 == 1

    def test_full_bad_info(self):
        save_api_data(self.json_case_full_bad_info, self.sport_name)
        assert 1 == 1