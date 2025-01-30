from sqlalchemy.orm import Session

from database.models import User


class UserDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_email(self, user_id):
        return self.db_session.query(User.email).filter(user_id=user_id).first()