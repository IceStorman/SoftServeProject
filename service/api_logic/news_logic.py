import json
from datetime import datetime
from enum import Enum
import numpy as np
import pandas as pd
from flask import Response
from sqlalchemy import desc
from database.models import News
from database.azure_blob_storage.save_get_blob import blob_get_news
from dto.api_output import OutputRecommendationList
from logger.logger import Logger


class ConstForRecommendations(Enum):
    SEC_PER_DAY = 86400
    PERIOD_OF_TIME = 21
    MAX_LIMIT_FOR_REC_IN_DAYS = 21
    SCORE_FOR_NOT_PREFER_SPORT = 0.25
    SCORE_FOR_PREFER_SPORT = 0.20
    SCORE_FOR_NOTHING = 0.1
    SCORE_FOR_PREFER_TEAM = 0.2
    BASE_LIMIT_OF_NEWS_FOR_RECS = 5
    MIN_PROMOTION_COF = 1
    MAX_PROMOTION_COF = 4


class NewsService:
    def __init__(self, news_dal, sport_dal, user_dal):
        self._news_dal = news_dal
        self._sport_dal = sport_dal
        self._user_dal = user_dal
        self._logger = Logger("logger", "all.log").logger
        self._recommendations_list = []


    def get_news_by_count(self, COUNT: int):
        news = self._news_dal.fetch_news(order_by=desc(News.save_at), limit=COUNT)
        return self.json_news(news)


    def get_latest_sport_news(self, COUNT: int, sport_name: str):
        sport = self._sport_dal.get_sport_by_name(sport_name)
        filters = [News.sport_id == sport.sport_id]
        news = self._news_dal.fetch_news(order_by=desc(News.save_at), limit=COUNT, filters=filters)
        return self.json_news(news)

    def get_popular_news(self, COUNT: int):
        news = self._news_dal.fetch_news(order_by=desc(News.interest_rate), limit=COUNT)
        return self.json_news(news)


    def get_news_by_id(self, blob_id: str):
        news = self._news_dal.get_news_by_blob_id(blob_id)
        if news:
            self._logger.warning(f"News were found: {news}")
            return self.json_news([news])


    def json_news(self, news_records):
        all_results = []
        for news_record in news_records:
            data = blob_get_news(news_record.blob_id)
            all_results.append({
                "blob_id": news_record.blob_id,
                "data": data
            })
        return Response(
            json.dumps(all_results, ensure_ascii=False),
            content_type='application/json; charset=utf-8',
        )


    async def retrieve_user_recommendations_from_blob(self, recommendations_list):
        all_news_from_blob = []
        for recs in recommendations_list:
            news_id = recs["news_id"]
            news_from_blob = self._news_dal.get_news_by_native_id(news_id)
            all_news_from_blob.append(news_from_blob)

        return self.json_news(all_news_from_blob)


    def user_recommendations_based_on_preferences_and_last_watch(self, user_id, top_n=ConstForRecommendations.BASE_LIMIT_OF_NEWS_FOR_RECS.value):
        user_preferred_teams, user_preferred_sports = self.__get_user_preferences(user_id)

        user_and_news_data = self._news_dal.get_user_interactions_with_news_by_period_of_time(
            user_id,
            period_of_time=ConstForRecommendations.PERIOD_OF_TIME.value
        )

        (
            user_interact_with_this_news_mask,
            user_not_interact_with_this_news_mask,
            user_and_news_details_df
        ) = self._news_dal.data_frame_to_work_with_user_and_news_data(user_and_news_data)

        news_coefficients = self.__calculating_news_coefficients_by_parameters_from_df_and_user_preferences(
            user_and_news_details_df,
            user_preferred_teams,
            user_preferred_sports,
            user_interact_with_this_news_mask
        )

        news_coefficients_without_duplicates = self._news_dal.cleaning_duplicate_news_where_is_more_than_one_club(news_coefficients)

        news_adjusted_score_df = self.__calculating_adjusted_score_for_by_coefficients_inside_df(news_coefficients_without_duplicates)

        user_saw_this_news_df, user_not_saw_this_news_df = self._news_dal.assign_adjusted_scores_for_masks(
            news_adjusted_score_df,
            user_interact_with_this_news_mask,
            user_not_interact_with_this_news_mask
        )

        recs_by_user_preferences = self.__get_recommendations_by_user_preferences(user_not_saw_this_news_df, top_n)

        recs_by_user_last_watch = self.__get_recommendations_by_last_watch_type(
            user_not_saw_this_news_df,
            user_saw_this_news_df,
            top_n
        )

        return self.__return_recommendations(
            user_not_saw_this_news_df,
            recs_by_user_preferences,
            recs_by_user_last_watch,
            user_id
        )


    def __get_user_preferences(self, user_id):
        user_preferences = self._user_dal.get_user_sport_and_club_preferences_by_native_id(user_id)

        if not user_preferences:
            return [], []

        user_preferred_teams = list({row.preferences for row in user_preferences if row.preferences is not None})
        user_preferred_sports = list({row.sports_id for row in user_preferences if row.sports_id is not None})

        return user_preferred_teams, user_preferred_sports


    def __calculate_time_score_vectorized(self, save_at, time_now=datetime.now()):
        delta_days = (time_now - save_at).dt.total_seconds() * (1 / ConstForRecommendations.SEC_PER_DAY.value)  # Помножили замість поділу
        return np.maximum(0, 1 - delta_days / ConstForRecommendations.MAX_LIMIT_FOR_REC_IN_DAYS.value)


    def __calculate_team_score_vectorized(self, teams_in_news, user_preferred_teams):
        return np.sum(np.isin(teams_in_news, user_preferred_teams)) * ConstForRecommendations.SCORE_FOR_PREFER_TEAM.value or ConstForRecommendations.SCORE_FOR_NOTHING.value


    def __calculate_sport_score_vectorized(self, news_sports, preferred_sports, user_interactions):
        preferred_count = np.sum(np.isin(news_sports, preferred_sports)) * ConstForRecommendations.SCORE_FOR_PREFER_SPORT.value
        interacted_count = np.sum(np.isin(news_sports, user_interactions)) * ConstForRecommendations.SCORE_FOR_NOT_PREFER_SPORT.value

        return preferred_count + interacted_count or ConstForRecommendations.SCORE_FOR_NOTHING.value


    def __calculating_news_coefficients_by_parameters_from_df_and_user_preferences(
            self,
            user_and_news_details_df,
            user_preferred_teams,
            user_preferred_sports,
            user_interact_with_this_news_mask
    ):
        user_and_news_details_df['time_score'] = self.__calculate_time_score_vectorized(
            user_and_news_details_df['save_at']
        )

        user_and_news_details_df['team_score'] = self.__calculate_team_score_vectorized(
            user_and_news_details_df['team_id'],
            user_preferred_teams
        )

        user_and_news_details_df['sport_score'] = user_and_news_details_df['sport_id'].apply(
            lambda sport: self.__calculate_sport_score_vectorized(
                [sport],
                user_preferred_sports,
                user_interact_with_this_news_mask['sport_id']
            )
        )

        user_and_news_details_df.drop(columns=['sport_id', 'save_at', 'team_id'], inplace=True)

        return user_and_news_details_df


    def __calculating_adjusted_score_for_by_coefficients_inside_df(self, dataframe):
        dataframe['adjusted_score'] = (
                dataframe['interest_rate_score'] *
                dataframe['time_score'] *
                dataframe['team_score'] *
                dataframe['sport_score']
        )
        return dataframe


    def __calculate_average_adjusted_score_by_last_watch_news_by_user(self, interacted_df, not_interacted_df):
        return (
            interacted_df['adjusted_score'].sum() / len(not_interacted_df)
            if len(interacted_df) > 0 else -1
        )


    def __get_recommendations_by_user_preferences(self, not_interacted_df, top_n):
        return not_interacted_df['adjusted_score'].sort_values(ascending=False).head(top_n).index.tolist()


    def __get_recommendations_by_last_watch_type(self, user_not_saw_this_news_df, user_saw_this_news_df, top_n):
        average_adjusted_score_by_last_watch_news = self.__calculate_average_adjusted_score_by_last_watch_news_by_user(
            user_saw_this_news_df,
            user_not_saw_this_news_df
        )
        if average_adjusted_score_by_last_watch_news == -1:
            return None

        return user_not_saw_this_news_df.iloc[
            (user_not_saw_this_news_df['adjusted_score'] - average_adjusted_score_by_last_watch_news).abs().argsort()[:top_n]
        ].index.tolist()


    def __return_recommendations(
            self,
            user_not_saw_this_news_df,
            recs_by_user_preferences,
            recs_by_user_last_watch,
            user_id
    ):
        recommendations_list_by_user_preferences = [
            {
                "news_id": news,
                "score": user_not_saw_this_news_df.loc[news, 'adjusted_score'],
                "user_id": user_id,
            }
            for news in recs_by_user_preferences
        ]
        recommendations_list_by_user_last_watch = [
            {
                "news_id": news,
                "score": user_not_saw_this_news_df.loc[news, 'adjusted_score'],
                "user_id": user_id,
            }
            for news in recs_by_user_last_watch
        ]
        self._news_dal.delete_dataframe(user_not_saw_this_news_df)
        self._news_dal.delete_dataframe(recs_by_user_preferences)
        self._news_dal.delete_dataframe(recs_by_user_last_watch)


        return {
            "recommendations_list_by_user_preferences": recommendations_list_by_user_preferences,
            "recommendations_list_by_user_last_watch": recommendations_list_by_user_last_watch
        }
