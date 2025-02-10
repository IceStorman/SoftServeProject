from datetime import datetime
from enum import Enum
import numpy as np
import pandas as pd


class RecommendationConsts(Enum):
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

class CalculatingHelper:


    def __calculate_time_score_vectorized(self, save_at: datetime, time_now: datetime = datetime.now()) -> pd.DataFrame:
        delta_days = (time_now - save_at).dt.total_seconds() * (1 / RecommendationConsts.SEC_PER_DAY.value)
        return np.maximum(0, 1 - delta_days / RecommendationConsts.MAX_LIMIT_FOR_REC_IN_DAYS.value)


    def __calculate_team_score_vectorized(self, teams_in_news: pd.DataFrame, user_preferred_teams: list[int]) -> pd.DataFrame:
        return np.sum(np.isin(teams_in_news, user_preferred_teams)) * RecommendationConsts.SCORE_FOR_PREFER_TEAM.value or RecommendationConsts.SCORE_FOR_NOTHING.value


    def __calculate_sport_score_vectorized(self, news_sports: list[int], preferred_sports: list[int], user_interactions: pd.DataFrame) -> pd.DataFrame:
        preferred_count = np.sum(np.isin(news_sports, preferred_sports)) * RecommendationConsts.SCORE_FOR_PREFER_SPORT.value
        interacted_count = np.sum(np.isin(news_sports, user_interactions)) * RecommendationConsts.SCORE_FOR_NOT_PREFER_SPORT.value

        return preferred_count + interacted_count or RecommendationConsts.SCORE_FOR_NOTHING.value


    def calculating_news_coefficients_by_parameters_from_df_and_user_preferences(
            self,
            user_and_news_details_df: pd.DataFrame,
            user_preferred_teams: list[int],
            user_preferred_sports: list[int],
            user_interact_with_this_news_mask: pd.DataFrame.mask
    ) -> pd.DataFrame:

        user_and_news_details_df['time_score'] = self.__calculate_time_score_vectorized(
            user_and_news_details_df['save_at']
        )

        user_and_news_details_df['team_score'] = user_and_news_details_df.apply(
            lambda row: self.__calculate_team_score_vectorized(
                row['team_id'],
                user_preferred_teams
            ),
            axis=1
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


    def calculating_adjusted_score_by_coefficients_inside_df(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe['adjusted_score'] = dataframe['interest_rate_score'] * dataframe['time_score'] * dataframe['team_score'] * dataframe['sport_score']
        return dataframe


    def calculate_user_average_adjusted_score_by_last_watch_news(self, interacted_df: pd.DataFrame, not_interacted_df: pd.DataFrame) -> pd.DataFrame:
        return (
            interacted_df['adjusted_score'].sum() / len(not_interacted_df)
            if len(interacted_df) > 0 else -1
        )
