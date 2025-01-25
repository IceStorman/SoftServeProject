from flask import current_app, url_for
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from dto.api_output import OutPutUser
from database.models import User
from exept.handle_exeptions import handle_exceptions
import bcrypt
from logger.logger import Logger

api_logic_logger = Logger("api_logic_logger", "api_logic_logger.log")


@handle_exceptions
@api_logic_logger.log_function_call()
class UserService:
    def __init__(self, user_dal):
        self.user_dal = user_dal
        self.s = URLSafeTimedSerializer(current_app.secret_key)


    def create_user(self, email_front, username_front, password_front):
        existing_user = self.user_dal.get_user_by_email_or_username(email_front, username_front)
        if existing_user:
            return OutPutUser().dump(existing_user)

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_front.encode('utf-8'), salt)

        new_user = User(email=email_front, username=username_front, password_hash=hashed_password)
        self.user_dal.create_user(new_user)

        return OutPutUser().dump(new_user)

    def request_password_reset(self, email: str):
        existing_user = self.user_dal.get_user_by_email(email)
        if not existing_user:
            return OutPutUser().dump(None)

        token = self.get_reset_token(existing_user.email)

        return self.send_reset_email(existing_user, token)

    def send_reset_email(self, user: User, token: str):
        try:
            reset_url = url_for('login_app.reset_password', token=token, _external=True)
            msg = Message(
                'Password Reset Request',
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[user.email]
            )
            msg.body = f'''To reset your password, visit the following link:
                        {reset_url}
                        If you did not make this request, please ignore this email. 222
                        '''
            current_app.extensions['mail'].send(msg)
            return {"msg": "Success"}
        except Exception as e:
            print(e)

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
