from datetime import datetime, timedelta
import pytest
import pandas as pd
import numpy as np
from service.api_logic.helpers.calculating_helper import CalculatingRecommendationHelper, RecommendationConsts


class TestCalculatingHelper:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.calculating_helper = CalculatingRecommendationHelper()


    def test_calculate_time_score_vectorized(self):
        now = datetime.now()
        save_at = pd.Series([now - timedelta(days=i) for i in range(100)])
        expected_scores = np.maximum(0, 1 - np.array(range(100)) / RecommendationConsts.MAX_LIMIT_FOR_REC_IN_DAYS.value)

        result = self.calculating_helper._CalculatingRecommendationHelper__calculate_time_score_vectorized(save_at, now)

        assert np.allclose(result, expected_scores)


    def test_calculate_team_score_vectorized(self):
        teams_in_news = pd.DataFrame({'team_id': [1, 2, 3, 4, 5]})
        user_preferred_teams = [2, 4]
        expected_scores = np.array(
            [0.1, RecommendationConsts.SCORE_FOR_PREFER_TEAM.value, 0.1, RecommendationConsts.SCORE_FOR_PREFER_TEAM.value,0.1])

        result = teams_in_news['team_id'].apply(
            lambda team: self.calculating_helper._CalculatingRecommendationHelper__calculate_team_score_vectorized([team], user_preferred_teams))

        assert np.all(result.values == expected_scores)


    def test_calculate_sport_score_vectorized(self):
        news_sports = [1, 2, 3, 4]
        preferred_sports = [2, 3]
        user_interactions = pd.DataFrame({'sport_id': [3, 4]})

        expected_score = (
                np.sum(np.isin(news_sports, preferred_sports)) * RecommendationConsts.SCORE_FOR_PREFER_SPORT.value +
                np.sum(np.isin(news_sports, user_interactions['sport_id'])) * RecommendationConsts.SCORE_FOR_NOT_PREFER_SPORT.value
        )

        result = self.calculating_helper._CalculatingRecommendationHelper__calculate_sport_score_vectorized(news_sports, preferred_sports, user_interactions)

        assert result == expected_score, "Sport score calculation is incorrect"


    def test_calculate_adjusted_score_by_coefficients_inside_df(self):
        df = pd.DataFrame({
            'interest_rate_score': [1, 2, 3],
            'time_score': [0.1, 0.9, 0.5],
            'team_score': [0.1, 0.5, 0.2],
            'sport_score': [1, 2, 3],
        })
        expected_scores = df['interest_rate_score'] * df['time_score'] * df['team_score'] * df['sport_score']

        result_df = self.calculating_helper.calculate_adjusted_score_by_coefficients_inside_df(df)

        assert np.allclose(result_df['adjusted_score'], expected_scores), "Adjusted score calculation is incorrect"


    def test_calculate_user_average_adjusted_score_by_last_watch_news(self):
        interacted_df = pd.DataFrame({'adjusted_score': [0.8, 0.6, 0.9]})
        not_interacted_df = pd.DataFrame({'adjusted_score': [0.5, 0.4]})
        expected_avg_score = interacted_df['adjusted_score'].sum() / len(not_interacted_df)

        result = self.calculating_helper.calculate_user_average_adjusted_score_by_last_watch_news(interacted_df, not_interacted_df)

        assert result == expected_avg_score, "User average adjusted score calculation is incorrect"


    def test_calculate_user_average_adjusted_score_by_last_watch_news_no_interactions(self):
        interacted_df = pd.DataFrame({'adjusted_score': []})
        not_interacted_df = pd.DataFrame({'adjusted_score': [0.5, 0.4]})

        result = self.calculating_helper.calculate_user_average_adjusted_score_by_last_watch_news(interacted_df, not_interacted_df)

        assert result == -1, "Average adjusted score for no interactions should return -1"


    def test_calculate_news_coefficients_by_parameters_from_df_and_user_preferences(self):
        user_and_news_details_df = pd.DataFrame(
            {'blob_id': ['lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                         'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                         'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                         'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                         'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json'],
             'sport_id': [2, 3, 4, 3, 6],
             'save_at': [datetime(2025, 3, 9, 22, 28, 23, 287946),
                         datetime(2025, 3, 9, 22, 28, 23, 287946),
                         datetime(2025, 3, 9, 22, 28, 23, 287946),
                         datetime(2025, 3, 9, 22, 28, 23, 287946),
                         datetime(2025, 3, 9, 22, 28, 23, 287946)],
             'team_id': [1, 2, 3, 2, 3],
             'interest_rate': [1, 1, 1, 1, 1],
             'interaction': [0, 0, 1, 1, 0],
             }, index=[1, 2, 3, 4, 8]
        )
        preferred_teams = [1, 2, 3, 4]
        preferred_sports = [2, 3]
        user_interact_with_this_news_mask = pd.DataFrame(
            {'sport_id': [4, 3]}, index=[3, 4]
        )

        result = self.calculating_helper.calculate_news_coefficients_by_parameters_from_df_and_user_preferences(
            user_and_news_details_df, preferred_teams, preferred_sports, user_interact_with_this_news_mask
        )
        expected_columns = {"time_score", "team_score", "sport_score"}

        assert isinstance(result, pd.DataFrame)
        assert expected_columns.issubset(result.columns)



