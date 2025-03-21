from unittest.mock import MagicMock
import pytest
from dependency_injector import providers, containers
from flask import Flask
from service.api_logic.user_logic import UserService


class TestContainer(containers.DeclarativeContainer):
    db_session = providers.Singleton(MagicMock)

    user_dal = providers.Singleton(MagicMock)
    preferences_dal = providers.Singleton(MagicMock)
    sport_dal = providers.Singleton(MagicMock)

    user_service = providers.Factory(
        UserService,
        user_dal=user_dal,
        preferences_dal=preferences_dal,
        sport_dal=sport_dal,
    )


class TestUserService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app.config["SECRET_KEY"] = "test_secret"
        self.app_context.push()
        self.container = TestContainer()
        self.user_service = self.container.user_service()


    def teardown(self):
        self.app_context.pop()


    def test_get_user_sport_and_club_preferences_success(self):
        with self.app.app_context():
            user_id = 9
            self.container.user_dal().get_user_sport_and_club_preferences_by_id.return_value = [
                MagicMock(preferences=1, sports_id=3),
                MagicMock(preferences=1, sports_id=4),
                MagicMock(preferences=1, sports_id=5),
                MagicMock(preferences=2, sports_id=3),
                MagicMock(preferences=2, sports_id=4),
                MagicMock(preferences=2, sports_id=5),
            ]

            teams, sports = self.user_service.get_user_sport_and_club_preferences(user_id)

            assert list(set(teams)) == teams
            assert list(set(sports)) == sports
            assert isinstance(sports, list)
            assert isinstance(teams, list)
            assert len(sports) == 3
            assert len(teams) == 2


    def test_get_user_sport_and_club_preferences_when_empty_preferences(self):
        with self.app.app_context():
            user_id = 9
            self.container.user_dal().get_user_sport_and_club_preferences.return_value = []

            teams, sports = self.user_service.get_user_sport_and_club_preferences(user_id)

            assert teams == []
            assert sports == []


    def test_get_user_sport_and_club_preferences_when_empty_sport_preferences(self):
        with self.app.app_context():
            user_id = 9
            self.container.user_dal().get_user_sport_and_club_preferences_by_id.return_value = [
                MagicMock(preferences=1, sports_id=None),
                MagicMock(preferences=1, sports_id=None),
                MagicMock(preferences=1, sports_id=None),
                MagicMock(preferences=2, sports_id=None),
                MagicMock(preferences=2, sports_id=None),
                MagicMock(preferences=2, sports_id=None),
            ]

            teams, sports = self.user_service.get_user_sport_and_club_preferences(user_id)

            assert list(set(teams)) == teams
            assert len(teams) == 2
            assert sports == []


    def test_get_user_sport_and_club_preferences_when_empty_team_preferences(self):
        with self.app.app_context():
            user_id = 9
            self.container.user_dal().get_user_sport_and_club_preferences_by_id.return_value = [
                MagicMock(preferences=None, sports_id=1),
                MagicMock(preferences=None, sports_id=2),
                MagicMock(preferences=None, sports_id=3),
                MagicMock(preferences=None, sports_id=4),
                MagicMock(preferences=None, sports_id=5),
                MagicMock(preferences=None, sports_id=6),
            ]

            teams, sports = self.user_service.get_user_sport_and_club_preferences(user_id)

            assert len(sports) == 6
            assert teams == []