from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from dto.api_output import OutPutUser, OutputPreferences
from database.models import User
from exept.handle_exeptions import handle_exceptions
import bcrypt
from logger.logger import Logger
from jinja2 import Environment, FileSystemLoader
import os
from flask_jwt_extended import create_access_token

api_logic_logger = Logger("api_logic_logger", "api_logic_logger.log")


@handle_exceptions
@api_logic_logger.log_function_call()
class UserService:
    def __init__(self, user_dal, preferences_dal):
        self._user_dal = user_dal
        self._preferences_dal = preferences_dal
        self._serializer = URLSafeTimedSerializer(current_app.secret_key)


    def create_user(self, email_front, username_front, password_front):
        existing_user = self._user_dal.get_user_by_email_or_username(email_front, username_front)
        if existing_user:
            return OutPutUser().dump(existing_user)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_front.encode('utf-8'), salt)

        new_user = User(email=email_front, username=username_front, password_hash=hashed_password.decode('utf-8'))
        self._user_dal.create_user(new_user)

        return OutPutUser().dump(new_user)

    def request_password_reset(self, email: str):
        existing_user = self._user_dal.get_user_by_email(email)
        if not existing_user:
            return OutPutUser().dump(None)

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
        return {"msg": "Success"}


    def get_reset_token(self, email) -> str:
        return self.serializer.dumps(email, salt="email-confirm")

    def reset_user_password(self, email, new_password: str) -> str:
        user = self._user_dal.get_user_by_email(email)
        if not user:
            return
        self._user_dal.update_user_password(user, new_password)
        new_jwt = create_access_token(identity=user.email)
        return new_jwt

    def confirm_token(self, token: str, expiration=3600):
        try:
            email = self.serializer.loads(token, salt="email-confirm", max_age=expiration)
        except:
            return False
        user = self._user_dal.get_user_by_email(email)

        return OutPutUser().dump(user)

    def log_in(self, email_or_username: str, password: str):

        user = self._user_dal.get_user_by_email_or_username_and_password(email_or_username, password)

        if user:
            token = self.generate_auth_token(user)
            return {"message": "Success", "token": token}

        return {"error": "Incorrect data"} #Тарас сказав

    def generate_auth_token(self, user):
        return self.serializer.dumps(user.email, salt="user-auth-token")

    def add_preferences(self, user_id, preferences):
        if not user_id or not isinstance(preferences, list):
            return None
        existing_sports = set(self._preferences_dal.get_all_preference_indexes())
        valid_preferences = [sport_id for sport_id in preferences if sport_id in existing_sports]

        if not valid_preferences:
            return {"msg": "No valid preferences"}

        self._preferences_dal.delete_all_preferences(user_id)
        self._preferences_dal.add_preferences(user_id, preferences)
        return {"msg": "Success"}

    def get_user_preferences(self, user_id):
        prefs = self._preferences_dal.get_user_preferences(user_id)
        shema = OutputPreferences(many=True).dump(prefs)

        return shema

    def get_all_preferences(self):
        return self._preferences_dal.get_all_preferences()

    def delete_preferences(self, user_id, preferences):
        if not user_id or not isinstance(preferences, list):
            return None
        self._preferences_dal.delete_preferences(user_id, preferences)
        return {"msg": "Success"}