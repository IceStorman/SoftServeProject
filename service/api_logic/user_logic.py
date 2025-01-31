from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from dto.api_output import OutputUser, OutputPreferences, OutputLogin
from database.models import User
from dto.common_responce import CommonResponse
from exept.exeptions import UserDoNotExistError, NotCorrectUsernameOrPasswordError
import bcrypt
from logger.logger import Logger
from jinja2 import Environment, FileSystemLoader
import os
from flask_jwt_extended import create_access_token

logger = Logger("api_logic_logger", "api_logic_logger.log")


@logger.log_function_call()
class UserService:
    def __init__(self, user_dal):
        self.user_dal = user_dal
        self.serializer = URLSafeTimedSerializer(current_app.secret_key)


    def create_user(self, email_front, username_front, password_front):
        existing_user = self.user_dal.get_user_by_email_or_username(email_front, username_front)
        if existing_user:
            return OutputUser().dump(existing_user)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_front.encode('utf-8'), salt)

        new_user = User(email=email_front, username=username_front, password_hash=hashed_password.decode('utf-8'))
        self.user_dal.create_user(new_user)

        return OutputUser().dump(new_user)

    def request_password_reset(self, email: str):
        existing_user = self.user_dal.get_user_by_email_or_username(email)
        if not existing_user:
            raise UserDoNotExistError(email)

        token = self.get_reset_token(existing_user.email)
        return self.send_reset_email(existing_user, token)

    def message_to_user_gmail(self, user: User, reset_url):
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        env = Environment(loader=FileSystemLoader(template_dir))
        template = env.get_template("reset_password_email.html")

        return template.render(username=user.username, reset_url=reset_url)

    def send_reset_email(self, user: User, token: str):
        reset_url = url_for('login_app.reset_password', token=token, _external=True)
        msg = Message(
            'Password Reset Request',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[user.email],
            html=self.message_to_user_gmail(user, reset_url)
        )
        current_app.extensions['mail'].send(msg)
        return CommonResponse().to_dict()

    def get_reset_token(self, email) -> str:
        user = self.user_dal.get_user_by_email_or_username(email)
        if not user:
            raise UserDoNotExistError(email)

        return self.serializer.dumps(user.username, salt="email-confirm")

    def reset_user_password(self, email, new_password: str) -> str:
        user = self.user_dal.get_user_by_email_or_username(email)
        if not user:
            raise UserDoNotExistError(email)

        self.user_dal.update_user_password(user, new_password)
        new_jwt = create_access_token(identity=user.email)
        return new_jwt

    def confirm_token(self, token: str, expiration=3600):
        username = self.serializer.loads(token, salt="email-confirm", max_age=expiration)
        user = self.user_dal.get_user_by_email_or_username(username)
        return OutputUser().dump(user)

    def log_in(self, email_or_username: str, password: str):
        user = self.user_dal.get_user_by_email_or_username_and_password(email_or_username, password)
        if not user:
            raise NotCorrectUsernameOrPasswordError()

        token = self.generate_auth_token(user)
        return OutputLogin(email=user.email, token=token, id=user.user_id)

    def generate_auth_token(self, user):
        return self.serializer.dumps(user.email, salt="user-auth-token")