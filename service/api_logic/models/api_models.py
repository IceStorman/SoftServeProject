from enum import Enum

REFRESH = "refresh"
JTI = 'jti'

class AuthStrategies(Enum):
    SIMPLE = "simple"
    GOOGLE = "google"


class SportPreferenceFields:
    def __init__(self):
        self.main_table = "UserPreference"
        self.related_table = "Sport"
        self.user_id_field = "users_id"
        self.type_id_field = "sports_id"
        self.related_name = "sport_name"
        self.related_logo = "sport_img"
        self.related_id = "sport_id"


class TeamPreferenceFields:
    def __init__(self):
        self.main_table = "UserClubPreferences"
        self.related_table = "TeamIndex"
        self.user_id_field = "users_id"
        self.type_id_field = "preferences"
        self.related_name = "name"
        self.related_logo = "logo"
        self.related_id = "team_index_id"


class InteractionTypes(Enum):
    LIKE = 1
    DISLIKE = 2
    READ = 3
    OPEN = 4
    COMMENT = 5