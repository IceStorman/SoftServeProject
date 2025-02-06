from flask import current_app, url_for, jsonify
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from dto.api_input import InputUserLogInDTO
from dto.api_output import OutputUser, OutputLogin
from database.models import User
from dto.common_response import CommonResponse, CommonResponseWithUser
from exept.exeptions import UserDoesNotExistError, UserAlreadyExistError
import bcrypt
from logger.logger import Logger
from jinja2 import Environment, FileSystemLoader
import os
from flask_jwt_extended import create_access_token,create_refresh_token, set_access_cookies, set_refresh_cookies
from service.api_logic.auth_strategy import AuthManager


class UserService:

    def __init__(self, user_dal):
        self._user_dal = user_dal
        self._serializer = URLSafeTimedSerializer(current_app.secret_key)
        self._logger = Logger("logger", "all.log").logger


    def get_user_by_email_or_username(self, email_front=None, username_front=None):
        return self._user_dal.get_user_by_email_or_username(email_front, username_front)


    async def create_user(self, email_front, username_front, password_front):
        existing_user = self.get_user_by_email_or_username(email_front, username_front)
        if existing_user:
            self._logger.debug("User already exist")
            raise UserAlreadyExistError(existing_user)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_front.encode('utf-8'), salt)

        new_user = User(email = email_front, username = username_front, password_hash = hashed_password.decode('utf-8'))
        self._user_dal.create_user(new_user)
        token = await self.__generate_auth_token(new_user)

        return OutputLogin(email = new_user.email, token = token, id = new_user.user_id)


    def request_password_reset(self, email: str):
        existing_user = self.get_user_by_email_or_username(email)
        if not existing_user:
            raise UserDoesNotExistError(email)

        token = self.__get_reset_token(existing_user.email)

        return self.__send_reset_email(existing_user, token)


    def __message_to_user_gmail(self, user: User, reset_url):
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        env = Environment(loader = FileSystemLoader(template_dir))
        template = env.get_template("reset_password_email.html")

        return template.render(username = user.username, reset_url = reset_url)


    def __send_reset_email(self, user: User, token: str):
        reset_url = url_for('login_app.reset_password', token = token, _external = True)
        msg = Message(
            'Password Reset Request',
            sender = current_app.config['MAIL_USERNAME'],
            recipients = [user.email],
            html = self.__message_to_user_gmail(user, reset_url)
        )
        current_app.extensions['mail'].send(msg)

        return CommonResponse().to_dict()


    def __get_reset_token(self, email) -> str:
        user = self.get_user_by_email_or_username(email)
        if not user:
            raise UserDoesNotExistError(email)

        return self._serializer.dumps(user.username, salt = "email-confirm")


    def reset_user_password(self, email, new_password: str):
        user = self.get_user_by_email_or_username(email)
        if not user:
            raise UserDoesNotExistError(email)

        self._user_dal.update_user_password(user, new_password)
        new_jwt = create_access_token(identity=user.email)
        new_refresh = create_refresh_token(identity=user.email)

        response = jsonify({"message": "Password reset successful"})
        set_access_cookies(response, new_jwt)
        set_refresh_cookies(response, new_refresh)

        return response


    def confirm_token(self, token: str, expiration=3600):
        username = self._serializer.loads(token, salt = "email-confirm", max_age = expiration)
        user = self.get_user_by_email_or_username(None, username)

        return OutputUser().dump(user)


    async def log_in(self, credentials: InputUserLogInDTO):
        login_context = AuthManager(self)
        user = await login_context.execute_log_in(credentials.auth_provider, credentials)
        response = await self.create_access_token_response(user)
        return response


    async def __generate_auth_token(self, user):
            return self._serializer.dumps(user.email, salt = "user-auth-token")


    def get_generate_auth_token(self, user):
        return self.__generate_auth_token(user)


    async def create_access_token_response(self, user):
        access_token = create_access_token(identity = user.email)
        response = CommonResponseWithUser(user_id = user.id, user_email = user.email).to_dict()
        response_json = jsonify(response)
        set_access_cookies(response_json, access_token)

        return response_json