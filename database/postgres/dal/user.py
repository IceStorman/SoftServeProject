from sqlalchemy import or_
from database.models import User


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

    def create_user(self, new_user):
        self.session.add(new_user)
        self.session.commit()