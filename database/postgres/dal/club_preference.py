from sqlalchemy.orm import Session
from sqlalchemy import text, cast, Unicode

from database.models import ClubPreference

class ClubPreferenceDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_subscribed_users_on_specific_teams(self, team_name):
        data = self.db_session.query(ClubPreference).filter(ClubPreference.preferences == team_name).all()

        user_ids = list()
        for preference in data:
            user_ids.append(preference.users_id)

        return user_ids