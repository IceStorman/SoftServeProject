from sqlalchemy.orm import Session

from database.models import User, TempSubscribersData, UserClubPreferences


class UserEmailDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_users_by_preference_index(self, preference_index):
        query = (
            self.db_session.query(User)
            .join(UserClubPreferences, User.user_id == UserClubPreferences.users_id)
            .filter(UserClubPreferences.preferences == preference_index)
            .all()
        )

        return query