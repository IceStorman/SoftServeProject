from flask import current_app, url_for, jsonify
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from dto.api_output import OutputUser, OutputPreferences, OutputLogin
from database.models import User
from dto.common_responce import CommonResponse, CommonResponseWithUser
from exept.exeptions import UserDoNotExistError, IncorrectUsernameOrEmailError, UserAlreadyExistError, \
    IncorrectPasswordError, IncorrectPreferencesError, NotUserIdOrPreferencesError
import bcrypt
from logger.logger import Logger
from jinja2 import Environment, FileSystemLoader
import os
from flask_jwt_extended import create_access_token, set_access_cookies


class UserService:

    def __init__(self, user_dal, preferences_dal):
        self._user_dal = user_dal
        self._preferences_dal = preferences_dal
        self._serializer = URLSafeTimedSerializer(current_app.secret_key)
        self.logger = Logger("logger", "all.log").logger


    async def create_user(self, email_front, username_front, password_front):
        existing_user = self._user_dal.get_user_by_email_or_username(email_front, username_front)
        if existing_user:
            self.logger.debug("User already exist")
            raise UserAlreadyExistError(existing_user)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_front.encode('utf-8'), salt)

        new_user = User(email = email_front, username = username_front, password_hash = hashed_password.decode('utf-8'))
        self._user_dal.create_user(new_user)
        token = await self.__generate_auth_token(new_user)

        return OutputLogin(email = new_user.email, token = token, id = new_user.user_id)


    def request_password_reset(self, email: str):
        existing_user = self._user_dal.get_user_by_email_or_username(email)
        if not existing_user:
            raise UserDoNotExistError(email)

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
        user = self._user_dal.get_user_by_email_or_username(email)
        if not user:
            raise UserDoNotExistError(email)

        return self._serializer.dumps(user.username, salt = "email-confirm")


    def reset_user_password(self, email, new_password: str) -> str:
        user = self._user_dal.get_user_by_email_or_username(email)
        if not user:
            raise UserDoNotExistError(email)

        self._user_dal.update_user_password(user, new_password)
        new_jwt = create_access_token(identity = user.email)

        return new_jwt


    def confirm_token(self, token: str, expiration=3600):
        username = self._serializer.loads(token, salt = "email-confirm", max_age = expiration)
        user = self._user_dal.get_user_by_email_or_username(None, username)

        return OutputUser().dump(user)


    async def log_in(self, email_or_username: str, password: str):
        user = self._user_dal.get_user_by_email_or_username(email_or_username, email_or_username)

        if not user:
            self.logger.warning("User does not exist")
            raise IncorrectUsernameOrEmailError()

        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            self.logger.warning("Passwords do not match")
            raise IncorrectPasswordError()

        token = await self.__generate_auth_token(user)

        return OutputLogin(email = user.email, token = token, id = user.user_id)


    async def __generate_auth_token(self, user):
        return self._serializer.dumps(user.email, salt = "user-auth-token")


    def google_auth(self, email):
        user = self._user_dal.get_user_by_email_or_username(email)
        if not user:
            user = User(email = email, username = email.split('@')[0])
            self._user_dal.create_user(user)

        token = self.__generate_auth_token(user)

        return OutputLogin(email = user.email, token = token, id = user.user_id)


    async def create_access_token_response(self, user):
        access_token = create_access_token(identity = user.email)
        response = CommonResponseWithUser(user_id = user.id, user_email = user.email).to_dict()
        response_json = jsonify(response)
        set_access_cookies(response_json, access_token)

        return response_json


    def add_preferences(self, user_id, preferences):
        if not user_id or not isinstance(preferences, list):
            raise NotUserIdOrPreferencesError()

        existing_sports = set(self._preferences_dal.get_all_preference_indexes())
        valid_preferences = [sport_id for sport_id in preferences if sport_id in existing_sports]

        if not valid_preferences:
            raise IncorrectPreferencesError()

        self._preferences_dal.delete_all_preferences(user_id)
        self._preferences_dal.add_preferences(user_id, preferences)

        return CommonResponse().to_dict()


    def get_user_preferences(self, user_id):
        prefs = self._preferences_dal.get_user_preferences(user_id)
        shema = OutputPreferences(many=True).dump(prefs)

        return shema


    def get_all_preferences(self):
        return self._preferences_dal.get_all_preferences()


    def delete_preferences(self, user_id, preferences):
        if not user_id or not isinstance(preferences, list):
            raise NotUserIdOrPreferencesError()

        self._preferences_dal.delete_preferences(user_id, preferences)
        return CommonResponse().to_dict()
