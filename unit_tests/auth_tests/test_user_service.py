from unittest.mock import AsyncMock, MagicMock
import bcrypt
import pytest
from dependency_injector import providers, containers
from flask import Flask
from database.models import User
from dto.api_input import InputUserLogInDTO
from exept.exeptions import UserAlreadyExistError, UserDoesNotExistError, IncorrectUserDataError, \
    IncorrectLogInStrategyError
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

        log_in_info = {
            "email_or_username": "andriy.kozovyi@gmail.com",
            "username": "Andrew",
            "password": "noPassword228",
            "auth_provider": "simple"
        }
        self.log_in_info = InputUserLogInDTO().load(log_in_info)

    def teardown(self):
        self.app_context.pop()


    @pytest.mark.asyncio
    async def test_sign_up_existing_user(self):
        with self.app.app_context():
            with pytest.raises(UserAlreadyExistError, match="User .* already exist"):
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


    @pytest.mark.asyncio
    async def test_log_in_simple(self):
        mock_user = MagicMock()
        mock_user.password_hash = bcrypt.hashpw("noPassword228".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        mock_user.email = "andriy.kozovyi@gmail.com"

        self.user_service.get_user_by_email_or_username = MagicMock(return_value=mock_user)
        self.user_service._refresh_dal.get_valid_tokens_by_user = MagicMock(
            return_value=("mock_access_token", "mock_refresh_token"))
        self.user_service.create_tokens = AsyncMock(return_value=("mock_access_token", "mock_refresh_token"))

        with self.app.app_context():
            result_with_existing_tokens = await self.user_service.log_in(self.log_in_info)

        self.user_service._refresh_dal.get_valid_tokens_by_user = MagicMock(return_value=(None, None))

        with self.app.app_context():
            result_without_existing_tokens = await self.user_service.log_in(self.log_in_info)

        assert result_with_existing_tokens.user_id is not None
        assert result_without_existing_tokens.user_id is not None


    @pytest.mark.asyncio
    async def test_user_does_not_exist_simple(self):
        self.user_service.get_user_by_email_or_username = MagicMock(return_value=None)

        with self.app.app_context():
            with pytest.raises(UserDoesNotExistError, match="User .* not exist"):
                await self.user_service.log_in(self.log_in_info)


    @pytest.mark.asyncio
    async def test_user_wrong_data_simple(self):
        mock_user = MagicMock()
        mock_user.password_hash = bcrypt.hashpw("Wrong".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        self.user_service.get_user_by_email_or_username = MagicMock(return_value=mock_user)
        with self.app.app_context():
            with pytest.raises(IncorrectUserDataError, match="Username/Email or password are not correct"):
                await self.user_service.log_in(self.log_in_info)


    @pytest.mark.asyncio
    async def test_user_wrong_data_simple(self):
        wrong_auth_strategy = {
            "auth_provider": "Taras"
        }
        dto = InputUserLogInDTO().load(wrong_auth_strategy)

        with self.app.app_context():
            with pytest.raises(IncorrectLogInStrategyError, match=".* is not a log in method in this app"):
                await self.user_service.log_in(dto)