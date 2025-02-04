from database.models import UserPreference, Sport, TeamIndex, ClubPreference
from dto.api_input import UpdateUserPreferencesDTO
from service.api_logic.sports_logic import get_all_sports


class PreferencesDAL:
    PREFERENCE_TYPE = {
        "sport": {
            "main_table": UserPreference,
            "related_table": Sport,
            "userId": "users_id",
            "typeId": "sports_id"
        },
        "team": {
            "main_table": ClubPreference,
            "related_table": TeamIndex,
            "userId": "users_id",
            "typeId": "preferences"
        }
    }

    def __init__(self, session=None):
        self.session = session


    def get_all_sport_preferences(self):
        return get_all_sports()


    '''SCRIPTS FOR FIRST ONE WITH STRATEGY'''
    def add_sport_preferences(self, user_id: int, preferences: list[int]):
        for pref in preferences:
            exists = self.session.query(UserPreference).filter_by(users_id=user_id, sports_id=pref).first()
            if not exists:
                new_pref = UserPreference(users_id=user_id, sports_id=pref)
                self.session.add(new_pref)
        self.session.commit()


    def add_team_preferences(self, user_id: int, preferences: list[int]):
        for pref in preferences:
            exists = self.session.query(ClubPreference).filter_by(users_id=user_id, preferences=pref).first()
            if not exists:
                new_pref = ClubPreference(users_id=user_id, preferences=pref)
                self.session.add(new_pref)
        self.session.commit()


    def get_user_team_preferences(self, user_id):
        user_prefs = (
            self.session.query(
                ClubPreference.users_id,
                ClubPreference.preferences,
                TeamIndex.name,
                TeamIndex.logo
            )
            .join(TeamIndex, ClubPreference.preferences == TeamIndex.team_index_id)
            .filter(ClubPreference.users_id == user_id)
            .all()
        )
        return user_prefs


    def get_user_sport_preferences(self, user_id):
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


    def delete_sport_preferences(self, user_id: int, preferences: list[int]):
        for pref in preferences:
            self.session.query(UserPreference).filter_by(sports_id=pref, users_id=user_id).delete()
        self.session.commit()


    def delete_team_preferences(self, user_id: int, preferences: list[int]):
        for pref in preferences:
            self.session.query(ClubPreference).filter_by(preferences=pref, users_id=user_id).delete()
        self.session.commit()


    def delete_all_sport_preferences(self, user_id: int):
        self.session.query(UserPreference).filter_by(users_id=user_id).delete()
        self.session.commit()


    def delete_all_team_preferences(self, user_id: int):
        self.session.query(ClubPreference).filter_by(users_id=user_id).delete()
        self.session.commit()


    def get_all_sport_preference_indexes(self) -> list:
        return [
            sport.sport_id for sport in
            self.session.query(Sport.sport_id).order_by(Sport.sport_name.asc()).all()
        ]

    def get_all_team_preference_indexes(self):
        return [
            team.team_id for team in
            self.session.query(TeamIndex.team_index_id).order_by(TeamIndex.name.asc()).all()
        ]

    '''SCRIPTS FOR SECOND ONE WITH DICT OF MODELS'''
    # def add_preferences(self, dto: UpdateUserPreferencesDTO, preferences: list[int]):
    #     strategy = self.PREFERENCE_TYPE.get(dto.type)
    #
    #     for pref in preferences:
    #         exists = self.session.query(strategy['main_table']).filter_by(strategy['userId']=user_id, strategy['typeId']=pref).first()
    #         if not exists:
    #             new_pref = UserPreference(users_id=user_id, sports_id=pref)
    #             self.session.add(new_pref)
    #     self.session.commit()