from exept.handle_exeptions import handle_exceptions
from logger.logger import Logger
from dto.api_output import OutputPreferences

api_logic_logger = Logger("api_logic_logger", "api_logic_logger.log")


@handle_exceptions
@api_logic_logger.log_function_call()
class PreferencesService:
    def __init__(self, preferences_dal):
        self.preferences_dal = preferences_dal

    def add_preferences(self, user_id, preferences):
        if not user_id or not isinstance(preferences, list):
            return None
        self.preferences_dal.delete_preferences(user_id, preferences)
        self.preferences_dal.add_preferences(user_id, preferences)
        return {"msg": "Success"}

    def get_preferences(self, user_id):
        prefs = self.preferences_dal.get_preferences(user_id)
        shema = OutputPreferences(many=True)
        return shema.dump(prefs)


    def delete_preferences(self, user_id, preferences):
        if not user_id or not isinstance(preferences, list):
            return None
        self.preferences_dal.delete_preferences(user_id, preferences)
        return {"msg": "Success"}