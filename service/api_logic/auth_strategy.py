from abc import ABC, abstractmethod
import bcrypt
import requests
from flask import current_app, request
from oauthlib.oauth2 import WebApplicationClient
from database.models import User
from dto.api_input import InputUserLogInDTO
from dto.api_output import OutputLogin
from exept.exeptions import IncorrectUserDataError, UserDoesNotExistError, IncorrectLogInStrategyError, \
    InvalidAuthenticationDataError
from typing import Generic, TypeVar
from service.api_logic.models.api_models import AuthStrategies

T = TypeVar("T")


class AuthHandler(ABC, Generic[T]):
    def __init__(self, user_service):
        self._user_service = user_service
    
    def __is_suspicious_login(self, user_id: int) -> bool:
        refresh_entry = self._user_service._refresh_dal.get_valid_refresh_token_by_user(user_id)
        if not refresh_entry:
            return False  

        current_ip = self._user_service._request_helper.get_country_from_ip()
        current_device = self._user_service._request_helper.get_user_device()

        suspicious_conditions = [
            refresh_entry.last_ip and refresh_entry.last_ip == current_ip,
            refresh_entry.last_device and refresh_entry.last_device != current_device,
            self._user_service._refresh_dal.is_nonce_used(user_id, refresh_entry.nonce)
        ]

        return any(suspicious_conditions)

    def is_suspicious_login(self, user_id: int) -> bool:
        return self.__is_suspicious_login(user_id)

    @abstractmethod
    def authenticate(self, credentials: T):
        pass


class AuthManager:
    def __init__(self, user_service):
        self._user_service = user_service
        self.strategies = {
            AuthStrategies.SIMPLE.value: SimpleAuthHandler(user_service = self._user_service),
            AuthStrategies.GOOGLE.value: GoogleAuthHandler(user_service = self._user_service),
        }

    async def execute_log_in(self, credentials: T):
        strategy = credentials.auth_provider
        if strategy not in self.strategies:
            raise IncorrectLogInStrategyError(strategy)

        login_strategy = await self.strategies[strategy].authenticate(credentials)
        return login_strategy


class SimpleAuthHandler(AuthHandler[T]):
    async def authenticate(self, credentials: T):
        user = self._user_service.get_user_by_email_or_username(credentials.email_or_username, credentials.email_or_username)

        if not user:
            self._user_service._logger.warning("User does not exist")
            raise UserDoesNotExistError(credentials.email_or_username)

        if not bcrypt.checkpw(credentials.password.encode('utf-8'), user.password_hash.encode('utf-8')):
            self._user_service._logger.warning("Some log in data is incorrect")
            raise IncorrectUserDataError()
        if not self.is_suspicious_login(user.user_id):
            self._user_service.revoke_all_refresh_and_access_tokens_for_user(user.user_id)

        token = await self._user_service.get_generate_auth_token(user)

        return OutputLogin(email = user.email, token = token, user_id= user.user_id, username = user.username, new_user = False)


class GoogleAuthHandler(AuthHandler[T]):
    async def authenticate(self, credentials: T):
        with current_app.app_context():
            client = WebApplicationClient(current_app.config['GOOGLE_CLIENT_ID'])
            token_url, headers, body = client.prepare_token_request(
                current_app.config['TOKEN_URL'],
                client_secret=current_app.config['GOOGLE_CLIENT_SECRET'],
                authorization_response=request.url,
                redirect_url=current_app.config['REDIRECT_URI']
            )
        token_response = requests.post(token_url, headers=headers, data=body)

        if not token_response.ok:
            raise InvalidAuthenticationDataError(credentials.auth_provider)

        client.parse_request_body_response(token_response.text)

        user_info_response = requests.get(
            current_app.config['USER_INFO_URL'],
            headers={'Authorization': f'Bearer {client.token["access_token"]}'}
        )

        if not user_info_response.ok:
            raise InvalidAuthenticationDataError(credentials.auth_provider)

        data = user_info_response.json()
        user_info = InputUserLogInDTO().load(data)

        user = self._user_service.get_user_by_email_or_username(email=user_info.email)
        output_login = OutputLogin(email=user_info.email, token=None, user_id=None, username=None, new_user=True)

        if not user:
            user = User(email=user_info.email, username=user_info.email.split('@')[0])
            self._user_service.create_user(user)
        else:
            output_login.new_user = False
            if self.is_suspicious_login(user.user_id):
                self._user_service.revoke_all_refresh_and_access_tokens_for_user(user.user_id)      

        token = await self._user_service.get_generate_auth_token(user)

        output_login.token = token
        output_login.user_id = user.user_id
        output_login.username = user.username

        return output_login
