from sqlalchemy.orm import Session

from database.models import ClubPreference

class ClubPreferenceDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_subscribed_users_on_specific_teams(self, team_name):
        return self.db_session.query(ClubPreference.users_id).filter(preferences=team_name).all()