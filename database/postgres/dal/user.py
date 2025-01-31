from sqlalchemy import or_
from database.models import User
import bcrypt

class UserDAL:
    def __init__(self, session=None):
        self.session = session

    def get_user_by_email_or_username(self, email=None, username=None):
        filters = []

        if email:
            filters.append(User.email == email)

        if username:
            filters.append(User.username == username)

        if not filters:
            return None

        return self.session.query(User).filter(or_(*filters)).first()

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


