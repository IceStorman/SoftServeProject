from abc import ABC, abstractmethod
from typing import Dict
import bcrypt
import requests
from flask import current_app, request
from itsdangerous import URLSafeTimedSerializer
from oauthlib.oauth2 import WebApplicationClient

from database.models import User
from dto.api_input import InputUserLoginDTO, InputUserByGoogleDTO
from dto.api_output import OutputLogin
from exept.exeptions import IncorrectUsernameOrEmailError, IncorrectPasswordError
from typing import Generic, TypeVar

from logger.logger import Logger

T = TypeVar("T")

class AuthStrategy(ABC, Generic[T]):
    def __init__(self, user_dal, serializer):
        self._user_dal = user_dal
        self._logger = Logger("logger", "all.log").logger
        self._serializer = serializer

    @abstractmethod
    def authenticate(self, credentials: T):
        pass


class AuthContext:
    def __init__(self, strategy: AuthStrategy):
        self._strategy = strategy

    async def execute_login(self, credentials: T):
        login_strategy = await self._strategy.authenticate(credentials)
        return login_strategy


class SimpleAuthStrategy(AuthStrategy[InputUserLoginDTO]):
    async def authenticate(self, credentials: InputUserLoginDTO):
        user = self._user_dal.get_user_by_email_or_username(credentials.email_or_username, credentials.email_or_username)

        if not user:
            self._logger.warning("User does not exist")
            raise IncorrectUsernameOrEmailError()

        if not bcrypt.checkpw(credentials.password_hash.encode('utf-8'), user.password_hash.encode('utf-8')):
            self._logger.warning("Passwords do not match")
            raise IncorrectPasswordError()

        token = await self.__generate_auth_token(user)

        return OutputLogin(email=user.email, token=token, id=user.user_id)

    async def __generate_auth_token(self, user):
            return self._serializer.dumps(user.email, salt = "user-auth-token")


class GoogleAuthStrategy(AuthStrategy[InputUserByGoogleDTO]):
    async def authenticate(self, credentials: InputUserByGoogleDTO):
        with current_app.app_context():
            client = WebApplicationClient(current_app.config['GOOGLE_CLIENT_ID'])
            token_url, headers, body = client.prepare_token_request(
                current_app.config['TOKEN_URL'],
                client_secret=current_app.config['GOOGLE_CLIENT_SECRET'],
                authorization_response=request.url,
                redirect_url=current_app.config['REDIRECT_URI']
            )
        token_response = requests.post(token_url, headers=headers, data=body)
        client.parse_request_body_response(token_response.text)

        user_info_response = requests.get(
            current_app.config['USER_INFO_URL'],
            headers={'Authorization': f'Bearer {client.token["access_token"]}'}
        )

        user_info = InputUserByGoogleDTO().load(user_info_response.json())

        user = self._user_dal.get_user_by_email_or_username(user_info.email)
        if not user:
            user = User(email=user_info.email, username=user_info.email.split('@')[0])
            self._user_dal.create_user(user)

        token = self.__generate_auth_token(user)

        return OutputLogin(email=user.email, token=token, id=user.user_id)

    async def __generate_auth_token(self, user):
            return self._serializer.dumps(user.email, salt = "user-auth-token")