from sqlalchemy import or_
from database.models import User
import bcrypt

class UserDAL:
    def __init__(self, session=None):
        self.session = session

    def get_user_by_email_or_username(self, email, username):
        return self.session.query(User).filter(
            or_(
                User.email == email,
                User.username == username
            )
        ).first()

    def get_user_by_email(self, email: str) -> User:
        return self.session.query(User).filter(User.email == email).first()

    def create_user(self, new_user):
        self.session.add(new_user)
        self.session.commit()

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter(User.user_id == user_id).first()

    def update_user_password(self, user: User, new_password):
        user.password_hash = new_password
        self.session.commit()

    def get_user_by_email_or_username_and_password(self, email_or_username, password):
        user = self.session.query(User).filter(
            or_(
                User.email == email_or_username,
                User.username == email_or_username
            )
        ).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            return user
        return None
