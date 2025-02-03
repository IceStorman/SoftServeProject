from abc import ABC, abstractmethod


class PreferenceStrategy(ABC):
    @abstractmethod
    def get_existing_preferences(self, dal):
        pass

    @abstractmethod
    def get_user_preferences(self, dal, user_id):
        pass

    @abstractmethod
    def delete_preferences(self, dal, user_id, preferences):
        pass

    @abstractmethod
    def add_preferences(self, dal, user_id, preferences):
        pass

    @abstractmethod
    def delete_all_preferences(self, dal, user_id):
        pass



class SportPreferenceStrategy(PreferenceStrategy):
    def get_existing_preferences(self, dal):
        return set(dal.get_all_sport_preference_indexes())


    def get_user_preferences(self, dal, user_id):
        return dal.get_user_sport_preferences(user_id)


    def delete_preferences(self, dal, user_id, preferences):
        dal.delete_sport_preferences(user_id, preferences)


    def add_preferences(self, dal, user_id, preferences):
        dal.add_sport_preferences(user_id, preferences)


    def delete_all_preferences(self, dal, user_id):
        dal.delete_all_sport_preferences(user_id)


class TeamPreferenceStrategy(PreferenceStrategy):
    def get_existing_preferences(self, dal):
        return set(dal.get_all_team_preference_indexes())


    def get_user_preferences(self, dal, user_id):
        return dal.get_user_team_preferences(user_id)


    def delete_preferences(self, dal, user_id, preferences):
        dal.delete_team_preferences(user_id, preferences)


    def add_preferences(self, dal, user_id, preferences):
        dal.add_team_preferences(user_id, preferences)


    def delete_all_preferences(self, dal, user_id):
        dal.delete_all_team_preferences(user_id)



