import json
from enum import Enum
import pandas as pd
from flask import Response
from sqlalchemy import desc
from database.models import News
from database.azure_blob_storage.save_get_blob import blob_get_news
from service.api_logic.scripts import get_sport_by_name
from logger.logger import Logger
from service.api_logic.filter_manager.filter_manager_factory import FilterManagerFactory
from dto.pagination import Pagination
from dto.api_input import NewsDTO
from service.api_logic.helpers.calculating_helper import CalculatingRecommendationHelper


class LimitsConsts(Enum):
    BASE_LIMIT_OF_NEWS_FOR_RECS = 5
    PERIOD_OF_TIME = 21


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

    def get_filtered_news(self, filters: NewsDTO):
        query = self._news_dal.get_query(News).order_by(desc(News.save_at))

        filtered_query = FilterManagerFactory.apply_filters(News, query, filters)

        news = self._news_dal.execute_query(filtered_query)
        return self.json_news(news)

    def user_recommendations_based_on_preferences_and_last_watch(
            self,
            user_id: int,
            user_preferred_teams,
            user_preferred_sports,
            calculating_helper: CalculatingRecommendationHelper,
            top_n: int = LimitsConsts.BASE_LIMIT_OF_NEWS_FOR_RECS.value
    ):

        user_interact_with_this_news_mask, user_not_interact_with_this_news_mask, user_and_news_details_df = (
            self._news_dal.data_frame_to_work_with_user_and_news_data(
                self._news_dal.get_user_interactions_with_news_by_period_of_time(
                        user_id,
                        period_of_time=LimitsConsts.PERIOD_OF_TIME.value
                )
            )
        )

        news_recommendation_coefficients_base_on_parametrs_insideDF = calculating_helper.calculate_news_coefficients_by_parameters_from_df_and_user_preferences(
            user_and_news_details_df,
            user_preferred_teams,
            user_preferred_sports,
            user_interact_with_this_news_mask,
        )

        news_with_adjusted_score_df = calculating_helper.calculate_adjusted_score_by_coefficients_inside_df(
            self._news_dal.clean_duplicate_news_where_is_more_than_one_club(
                news_recommendation_coefficients_base_on_parametrs_insideDF
            )
        )

        user_saw_this_news_df, user_not_saw_this_news_df = self._news_dal.assign_adjusted_scores_for_masks(
            news_with_adjusted_score_df,
            user_interact_with_this_news_mask,
            user_not_interact_with_this_news_mask
        )

        recs_by_user_preferences = self.__get_recommendations_by_user_preferences(user_not_saw_this_news_df, top_n)

        recs_by_user_last_watch = self.__get_recommendations_by_last_watch_type(
            user_not_saw_this_news_df,
            user_saw_this_news_df,
            calculating_helper,
            top_n
        )

        return (
            user_not_saw_this_news_df,
            recs_by_user_preferences,
            recs_by_user_last_watch
        )


    def __get_recommendations_by_user_preferences(self, not_interacted_df: pd.DataFrame, top_n: int) -> list[int]:
        return not_interacted_df['adjusted_score'].sort_values(ascending=False).head(top_n).index.tolist()


    def __get_recommendations_by_last_watch_type(
            self,
            user_not_saw_this_news_df: pd.DataFrame,
            user_saw_this_news_df: pd.DataFrame,
            calculating_helper: CalculatingRecommendationHelper,
            top_n: int
    ) -> pd.DataFrame | None:

        if len(user_not_saw_this_news_df) >= 0:
            average_adjusted_score_by_last_watch_news = calculating_helper.calculate_user_average_adjusted_score_by_last_watch_news(
                user_saw_this_news_df,
                user_not_saw_this_news_df
            )

            if average_adjusted_score_by_last_watch_news == -1:
                return None

        return user_not_saw_this_news_df.iloc[
            (user_not_saw_this_news_df['adjusted_score'] - average_adjusted_score_by_last_watch_news).abs().argsort()[:top_n]
        ].index.tolist()
