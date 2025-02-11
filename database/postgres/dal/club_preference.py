from sqlalchemy.orm import Session
from sqlalchemy import text, cast, Unicode

from database.models import UserClubPreferences

class UserClubPreferenceDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session