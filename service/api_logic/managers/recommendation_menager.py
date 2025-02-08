import pandas as pd
from database.azure_blob_storage.save_get_blob import blob_get_news
from service.api_logic.helpers.calculating_helper import CalculatingHelper
from service.api_logic.news_logic import NewsService
from service.api_logic.user_logic import UserService


class RecommendationManager:
    def __init__(self, user_service: UserService, news_service: NewsService):
        self.user_service = user_service
        self.news_service = news_service
        self.calculating_helper = CalculatingHelper()

    def get_recommended_news_for_user(self, user_id: int):
        preferred_teams, preferred_sports = self.user_service.get_user_sport_and_club_preferences(user_id)

        user_not_saw_this_news_df, recs_by_user_preferences, recs_by_user_last_watch = self.news_service.user_recommendations_based_on_preferences_and_last_watch(
            user_id,
            preferred_teams,
            preferred_sports,
            self.calculating_helper
        )

        return self.__final_user_recommendations(
             user_not_saw_this_news_df,
             recs_by_user_preferences,
             recs_by_user_last_watch,
             user_id
        )


    def __final_user_recommendations(
            self,
            user_not_saw_this_news_df: pd.DataFrame,
            recs_by_user_preferences: list[int],
            recs_by_user_last_watch: pd.DataFrame,
            user_id: int
    ):
        recommendations_list_by_user_preferences = [
            {
                "news_id": news,
                "score": user_not_saw_this_news_df.loc[news, 'adjusted_score'],
                "user_id": user_id,
                "article": self.__retrieve_user_recommendations_from_blob(user_not_saw_this_news_df.loc[news, 'blob_id'])
            }
            for news in recs_by_user_preferences
        ]
        recommendations_list_by_user_last_watch = [
            {
                "news_id": news,
                "score": user_not_saw_this_news_df.loc[news, 'adjusted_score'],
                "user_id": user_id,
                "article":  self.__retrieve_user_recommendations_from_blob(user_not_saw_this_news_df.loc[news, 'blob_id'])
            }
            for news in recs_by_user_last_watch
        ]

        return {
            "recommendations_list_by_user_preferences": recommendations_list_by_user_preferences,
            "recommendations_list_by_user_last_watch": recommendations_list_by_user_last_watch
        }


    def __retrieve_user_recommendations_from_blob(self, blob_id):
        data = blob_get_news(blob_id)
        return {
            "blob_id": blob_id,
            "data": data
        }

