import pytest
from unittest.mock import MagicMock
import pandas as pd
from service.api_logic.managers.recommendation_menager import RecommendationManager
from exept.exeptions import UserDoesNotExistError


class TestRecommendationManager:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.user_service = MagicMock()
        self.news_service = MagicMock()
        self.user_dal = MagicMock()
        self.manager = RecommendationManager(self.user_service, self.news_service, self.user_dal)


    def test_get_recommended_news_for_user_success(self):
        self.user_dal.get_user_id_by_email.return_value = [42]
        self.user_service.get_user_sport_and_club_preferences.return_value = ([2,3,4], [1,2,4,5])

        user_unseen_news_df = pd.DataFrame(
            {"blob_id": [
                'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                'transfer-rumors--news--real-madrid-look-at-arsenal-s-saliba---espn.json'
                ], "adjusted_score": [0.9, 0.8], 'sport_id': [2,4]}, index=[1, 2]
        )

        self.news_service.user_recommendations_based_on_preferences_and_last_watch.return_value = (
            user_unseen_news_df, [1, 2], [1]
        )

        result = self.manager.get_recommended_news_for_user("user@example.com")

        assert "recommendations_list_by_user_preferences" in result, "Поле 'recommendations_list_by_user_preferences' відсутнє"
        assert "recommendations_list_by_user_last_watch" in result, "Поле 'recommendations_list_by_user_last_watch' відсутнє"
        assert len(result["recommendations_list_by_user_preferences"]) == 2, "В цьому випадку поле 'recommendations_list_by_user_preferences' мало мати 2 результати"
        assert isinstance(result["recommendations_list_by_user_last_watch"], list), "'recommendations_list_by_user_last_watch' має бути списком"
        assert all("article" in item for item in result["recommendations_list_by_user_last_watch"]), "Деякі елементи не містять 'article'"


    def test_get_recommended_news_for_user_not_found(self):
        self.user_dal.get_user_id_by_email.return_value = []

        with pytest.raises(UserDoesNotExistError):
            self.manager.get_recommended_news_for_user("unknown@example.com")


    def test_get_recommended_news_for_user_empty_recommendations(self):
        self.user_dal.get_user_id_by_email.return_value = [42]
        self.user_service.get_user_sport_and_club_preferences.return_value = ([], [])

        user_unseen_news_df = pd.DataFrame({"blob_id": [], "adjusted_score": []})
        self.news_service.user_recommendations_based_on_preferences_and_last_watch.return_value = (
            user_unseen_news_df, [], None
        )

        result = self.manager.get_recommended_news_for_user("user@example.com")

        assert "recommendations_list_by_user_preferences" in result
        assert "recommendations_list_by_user_last_watch" in result
        assert len(result["recommendations_list_by_user_preferences"]) == 0
        assert len(result["recommendations_list_by_user_last_watch"]) == 0


    def test_a(self):
        assert 5 * 5 == 25

