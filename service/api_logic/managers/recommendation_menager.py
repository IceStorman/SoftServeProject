import pandas as pd
from database.azure_blob_storage.save_get_blob import blob_get_news, blob_get_news_bulk
from database.postgres.dal.user import UserDAL
from exept.exeptions import UserDoesNotExistError
from service.api_logic.helpers.calculating_helper import CalculatingRecommendationHelper
from service.api_logic.news_logic import NewsService
from service.api_logic.user_logic import UserService


class RecommendationManager:
    def __init__(self, user_service: UserService, news_service: NewsService, user_dal: UserDAL):
        self.user_service = user_service
        self.news_service = news_service
        self.user_dal = user_dal
        self.calculating_helper = CalculatingRecommendationHelper()


    def get_recommended_news_for_user(self, user_email: str):
        user_id = self.user_dal.get_user_id_by_email(user_email)
        if not user_id:
            raise UserDoesNotExistError(user_id)
        preferred_teams, preferred_sports = self.user_service.get_user_sport_and_club_preferences(user_id[0])

        user_unseen_news_df, recs_by_user_preferences, recs_by_user_last_watch = self.news_service.user_recommendations_based_on_preferences_and_last_watch(
            user_id[0],
            preferred_teams,
            preferred_sports,
            self.calculating_helper
        )

        return self.__get_final_user_recommendations(
             user_unseen_news_df,
             recs_by_user_preferences,
             recs_by_user_last_watch,
             user_id[0]
        )


    def __get_final_user_recommendations(
            self,
            user_not_saw_this_news_df: pd.DataFrame,
            recs_by_user_preferences: list[int],
            recs_by_user_last_watch: pd.DataFrame,
            user_id: int
    ):

        blob_data_by_user_preferences = blob_get_news_bulk(
            list(user_not_saw_this_news_df.loc[recs_by_user_preferences, 'blob_id'])
        )

        recommendations_list_by_user_preferences = [
            {
                "news_id": news,
                "score": user_not_saw_this_news_df.loc[news, 'adjusted_score'],
                "user_id": user_id,
                "article": blob_data_by_user_preferences.get(user_not_saw_this_news_df.loc[news, 'blob_id']),
            }
            for news in recs_by_user_preferences
        ]

        if recs_by_user_last_watch is None:
            recs_by_user_last_watch = recs_by_user_preferences

        blob_data_by_last_watch = blob_get_news_bulk(
            list(user_not_saw_this_news_df.loc[recs_by_user_last_watch, 'blob_id'])
        )

        recommendations_list_by_user_last_watch = [
            {
                "news_id": news,
                "score": user_not_saw_this_news_df.loc[news, 'adjusted_score'],
                "user_id": user_id,
                "article": blob_data_by_last_watch.get(user_not_saw_this_news_df.loc[news, 'blob_id'])
            }
            for news in recs_by_user_last_watch
        ]

        return {
            "recommendations_list_by_user_preferences": recommendations_list_by_user_preferences,
            "recommendations_list_by_user_last_watch": recommendations_list_by_user_last_watch
        }