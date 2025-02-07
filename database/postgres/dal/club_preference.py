from sqlalchemy.orm import Session
from sqlalchemy import text, cast, Unicode

from database.models import UserClubPreferences

class UserClubPreferenceDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_subscribed_users_on_specific_teams(self, team_index):
        data = self.db_session.query(UserClubPreferences).filter(UserClubPreferences.preferences == team_index).all()

        user_ids = list()
        for preference in data:
            user_ids.append(preference.users_id)

        return user_ids