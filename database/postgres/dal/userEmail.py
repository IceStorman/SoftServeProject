from sqlalchemy.orm import Session

from database.models import User


class UserEmailDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_email(self, user_id):
        data = self.db_session.query(User).filter(User.user_id == user_id).first()
        return data.email if data else None