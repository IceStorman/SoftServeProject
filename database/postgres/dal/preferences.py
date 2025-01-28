from database.models import UserPreference

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

    def get_preferences(self, user_id):
        return self.session.query(UserPreference).filter_by(users_id=user_id).all()

    def delete_preferences(self, user_id: int, preferences: list[int]):
        for pref in preferences:
            self.session.query(UserPreference).filter_by(sports_id=pref, users_id=user_id).delete()
        self.session.commit()