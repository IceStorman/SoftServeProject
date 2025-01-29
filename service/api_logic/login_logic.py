from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from dto.api_output import OutPutUser, OutputPreferences
from database.models import User
from exept.handle_exeptions import handle_exceptions
import bcrypt
from logger.logger import Logger

api_logic_logger = Logger("api_logic_logger", "api_logic_logger.log")

def message_to_user_gmail(user: User, reset_url):
    return  f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; border: 1px solid #ddd; border-radius: 10px; padding: 20px;">
                <h2 style="color: #4CAF50; text-align: center;">Password Reset Request</h2>
                <p>Dear <strong>{user.username}</strong>,</p>
                <p>You have requested to reset your password. To do so, click the button below:</p>
                <div style="text-align: center; margin: 20px 0;">
                    <a href="{reset_url}" style="display: inline-block; background-color: #4CAF50; color: white; text-decoration: none; padding: 10px 20px; border-radius: 5px; font-size: 16px;">Reset Your Password</a>
                </div>
                <p>If the button above doesn't work, copy and paste the following link into your browser:</p>
                <p style="word-break: break-word;">
                    <a href="{reset_url}" style="color: #4CAF50;">{reset_url}</a>
                </p>
                <p>If you did not request a password reset, please ignore this email or contact support.</p>
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                <p style="text-align: center; color: #777; font-size: 12px;">
                    Best regards,<br>
                    <strong>Your QSport Team</strong>
                </p>
            </div>
        </body>
    </html>
    """


@handle_exceptions
@api_logic_logger.log_function_call()
class UserService:
    def __init__(self, user_dal, preferences_dal):
        self.user_dal = user_dal
        self.preferences_dal = preferences_dal
        self.s = URLSafeTimedSerializer(current_app.secret_key)


    def create_user(self, email_front, username_front, password_front):
        existing_user = self.user_dal.get_user_by_email_or_username(email_front, username_front)
        if existing_user:
            return OutPutUser().dump(existing_user)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_front.encode('utf-8'), salt)

        new_user = User(email=email_front, username=username_front, password_hash=hashed_password.decode('utf-8'))
        self.user_dal.create_user(new_user)

        return OutPutUser().dump(new_user)

    def request_password_reset(self, email: str):
        existing_user = self.user_dal.get_user_by_email(email)
        if not existing_user:
            return OutPutUser().dump(None)

        token = self.get_reset_token(existing_user.email)

        return self.send_reset_email(existing_user, token)

    def send_reset_email(self, user: User, token: str):
        reset_url = url_for('login_app.reset_password', token=token, _external=True)
        msg = Message(
            'Password Reset Request',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[user.email],
            html=message_to_user_gmail(user, reset_url)
        )
        current_app.extensions['mail'].send(msg)
        return {"msg": "Success"}


    def get_reset_token(self, email) -> str:
        return self.s.dumps(email, salt="email-confirm")

    def reset_user_password(self, email, new_password: str) -> None:
        user = self.user_dal.get_user_by_email(email)
        self.user_dal.update_user_password(user, new_password)

    def confirm_token(self, token: str, expiration=3600):
        try:
            email = self.s.loads(token, salt="email-confirm", max_age=expiration)
        except:
            return False
        user = self.user_dal.get_user_by_email(email)
        return OutPutUser().dump(user)

    def log_in(self, email_or_username: str, password: str):

        user = self.user_dal.get_user_by_email_or_username_and_password(email_or_username, password)

        if user:
            token = self.generate_auth_token(user)
            return {"message": "Успішний вхід", "token": token}

        return {"error": "Невірні облікові дані"}

    def generate_auth_token(self, user):
        return self.s.dumps(user.email, salt="user-auth-token")

    def add_preferences(self, user_id, preferences):
        if not user_id or not isinstance(preferences, list):
            return None
        self.preferences_dal.delete_all_preferences(user_id)
        self.preferences_dal.add_preferences(user_id, preferences)
        return {"msg": "Success"}

    def get_user_preferences(self, user_id):
        prefs = self.preferences_dal.get_user_preferences(user_id)
        shema = OutputPreferences(many=True).dump(prefs)

        return shema

    def get_all_preferences(self):
        return self.preferences_dal.get_all_preferences()

    def delete_preferences(self, user_id, preferences):
        if not user_id or not isinstance(preferences, list):
            return None
        self.preferences_dal.delete_preferences(user_id, preferences)
        return {"msg": "Success"}
