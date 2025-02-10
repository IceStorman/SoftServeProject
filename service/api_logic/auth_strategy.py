from abc import ABC, abstractmethod
from enum import Enum
import bcrypt
import requests
from flask import current_app, request
from oauthlib.oauth2 import WebApplicationClient
from database.models import User
from dto.api_input import InputUserLogInDTO
from dto.api_output import OutputLogin
from exept.exeptions import IncorrectUserDataError, UserDoesNotExistError, IncorrectLogInStrategyMethodError, \
    InvalidAuthenticationDataError
from typing import Generic, TypeVar

T = TypeVar("T")

class AuthMethods(Enum):
    SIMPLE = "simple"
    GOOGLE = "google"


class AuthHandler(ABC, Generic[T]):
    def __init__(self, user_service):
        self._user_service = user_service

    @abstractmethod
    def authenticate(self, credentials: T):
        pass


class AuthManager:
    def __init__(self, user_service):
        self._user_service = user_service
        self.strategies = {
            AuthMethods.SIMPLE.value: SimpleAuthHandler(user_service=self._user_service),
            AuthMethods.GOOGLE.value: GoogleAuthHandler(user_service=self._user_service),
        }

    async def execute_log_in(self, method: str, credentials: T):
        if method not in self.strategies:
            raise IncorrectLogInStrategyMethodError(method)

        login_strategy = await self.strategies[method].authenticate(credentials)
        return login_strategy


class SimpleAuthHandler(AuthHandler[T]):
    async def authenticate(self, credentials: T):
        user = self._user_service.get_user_by_email_or_username(credentials.email_or_username, credentials.email_or_username)

        if not user:
            self._user_service._logger.warning("User does not exist")
            raise UserDoesNotExistError(user.email)

        if not bcrypt.checkpw(credentials.password_hash.encode('utf-8'), user.password_hash.encode('utf-8')):
            self._user_service._logger.warning("Passwords do not match")
            raise IncorrectUserDataError()

        token = await self._user_service.get_generate_auth_token(user)

        return OutputLogin(email=user.email, token=token, id=user.user_id)


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
        if token_response.status_code != 200:
            raise InvalidAuthenticationDataError()

        client.parse_request_body_response(token_response.text)

        user_info_response = requests.get(
            current_app.config['USER_INFO_URL'],
            headers={'Authorization': f'Bearer {client.token["access_token"]}'}
        )
        if user_info_response.status_code != 200:
            raise InvalidAuthenticationDataError()

        data = user_info_response.json()
        user_info = InputUserLogInDTO().load(data)

        user = self._user_service.get_user_by_email_or_username(user_info.email)
        if not user:
            user = User(email=data.email, username=data.email.split('@')[0])
            self._user_service.create_user(user)

        token = await self._user_service.get_generate_auth_token(user)

        return OutputLogin(email=user.email, token=token, id=user.user_id)