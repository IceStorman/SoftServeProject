from database.models import UserPreference, Sport
from service.api_logic.sports_logic import get_all_sports

class PreferencesDAL:

    def __init__(self, session=None):
        self.session = session


    def add_preferences(self, user_id: int, preferences: list[int]):
        for pref in preferences:
            exists = self.session.query(UserPreference).filter_by(users_id=user_id, sports_id=pref).first()
            if not exists:
                new_pref = UserPreference(users_id=user_id, sports_id=pref)
                self.session.add(new_pref)
        self.session.commit()


    def get_user_preferences(self, user_id):
        user_prefs = (
            self.session.query(
                UserPreference.users_id,
                UserPreference.sports_id,
                Sport.sport_name,
                Sport.sport_img
            )
            .join(Sport, UserPreference.sports_id == Sport.sport_id)
            .filter(UserPreference.users_id == user_id)
            .all()
        )
        return user_prefs


    def delete_preferences(self, user_id: int, preferences: list[int]):
        for pref in preferences:
            self.session.query(UserPreference).filter_by(sports_id=pref, users_id=user_id).delete()
        self.session.commit()


    def delete_all_preferences(self, user_id: int):
        self.session.query(UserPreference).filter_by(users_id=user_id).delete()
        self.session.commit()


    def get_all_preferences(self):
        return get_all_sports()


    def get_all_preference_indexes(self) -> list:
        return [
            sport.sport_id for sport in
            self.session.query(Sport.sport_id).order_by(Sport.sport_name.asc()).all()
        ]
