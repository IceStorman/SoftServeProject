from unittest.mock import AsyncMock, MagicMock
import pytest
from dependency_injector import providers, containers
from flask import Flask

from database.models import User
from dto.api_output import OutputLogin
from exept.exeptions import UserAlreadyExistError
from service.api_logic.user_logic import UserService


class TestContainer(containers.DeclarativeContainer):
    db_session = providers.Singleton(MagicMock)

    user_dal = providers.Singleton(MagicMock)
    preferences_dal = providers.Singleton(MagicMock)
    sport_dal = providers.Singleton(MagicMock)
    access_tokens_dal = providers.Singleton(MagicMock)
    refresh_dal = providers.Singleton(MagicMock)

    user_service = providers.Factory(
        UserService,
        user_dal=user_dal,
        preferences_dal=preferences_dal,
        sport_dal=sport_dal,
        access_tokens_dal=access_tokens_dal,
        refresh_dal=refresh_dal
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


    @pytest.mark.asyncio
    async def test_sign_up_existing_user(self):
        with self.app.app_context():
            with pytest.raises(UserAlreadyExistError, match="User .* exist"):
                await self.user_service.sign_up_user(email="andriy.kozovyi@gmail.com", username="Andrew",
                                                     password="noPassword")


    @pytest.mark.asyncio
    async def test_sign_up_new_user(self):
        self.user_service.get_existing_user = MagicMock(return_value=None)
        self.user_service.create_tokens = AsyncMock(return_value=("mocked_access_token", "mocked_refresh_token"))
        self.user_service.create_user = MagicMock()

        with self.app.app_context():
            result = await self.user_service.sign_up_user(
                email="taras228@gmail.com", username="Taras22", password="noPassword228"
            )

            assert result.user_id is not None


    def test_create_user(self):
        result = self.user_service.create_user(User(email="taras228@gmail.com", username="taras228", password_hash="someHash"))

        assert result.user_id is not None


    def test_get_user(self):
        result = self.user_service.get_user_by_email_or_username(email="andriy.kozovyi@gmail.com")

        assert result.user_id is not None