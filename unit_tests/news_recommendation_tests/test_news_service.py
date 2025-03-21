from unittest.mock import MagicMock
from datetime import datetime
import pandas as pd
import pytest
from dependency_injector import providers, containers
from flask import Flask
from service.api_logic.news_logic import NewsService


class TestContainer(containers.DeclarativeContainer):
    db_session = providers.Singleton(MagicMock)

    user_dal = providers.Singleton(MagicMock)
    news_dal = providers.Singleton(MagicMock)
    sport_dal = providers.Singleton(MagicMock)

    news_service = providers.Factory(
        NewsService,
        news_dal=news_dal,
        sport_dal=sport_dal,
        user_dal=user_dal,
    )


class TestNewsService:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app.config["SECRET_KEY"] = "test_secret"
        self.app_context.push()
        self.container = TestContainer()
        self.news_service = self.container.news_service()

        self.user_not_interact_with_this_news_mask = pd.DataFrame(
                {'sport_id': [2,3,6]}, index=[1,2,8]
            )

        self.user_interact_with_this_news_mask = pd.DataFrame(
            {'sport_id': [4, 3]}, index=[3, 4]
        )

        self.user_and_news_details_df = pd.DataFrame(
                {'blob_id': ['lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                             'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                             'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                             'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                             'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json'],
                 'sport_id': [2,3,4,3,6],
                 'save_at': [datetime(2025, 3, 9, 22, 28, 23, 287946),
                             datetime(2025, 3, 9, 22, 28, 23, 287946),
                             datetime(2025, 3, 9, 22, 28, 23, 287946),
                             datetime(2025, 3, 9, 22, 28, 23, 287946),
                             datetime(2025, 3, 9, 22, 28, 23, 287946)],
                 'team_index_id': [1,2,3,2,3],
                 'interest_rate': [1, 1,1,1,1],
                 'interaction': [0,0,1,1,0],
                 }, index=[1,2,3,4,8]
            )

        self.news_recommendation_coefficients_base_on_parametrs_insideDF = pd.DataFrame(
                {'blob_id': ['lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                             'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                             'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                             'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                             'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json'],
                 'interest_rate_score': [1, 1, 1, 1, 1],
                 'interaction_score': [0, 0, 1, 1, 0],
                 'time_score': ['0.1', '0.2', '0.11', '0.1', '0.4'],
                 'team_score': [0.1, 0.2, 0.1, 0.2, 0.1],
                 'sport_score': [0.2, 0.1, 0.1, 0.1, 0.2],
                 }, index=[1, 2, 3, 4, 8]
            )

        self.news_with_adjusted_score_df = pd.DataFrame(
            {'blob_id': ['lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                         'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                         'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                         'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                         'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json'],
             'interest_rate_score': [1, 1, 1, 1, 1],
             'interaction_score': [0, 0, 1, 1, 0],
             'time_score': [0.1, 0.2, 0.11, 0.1, 0.4],
             'team_score': [0.1, 0.2, 0.1, 0.2, 0.1],
             'sport_score': [0.2, 0.1, 0.1, 0.1, 0.2],
             'adjusted_score': [0.1, 0.2, 0.1, 0.1, 0.2],
             }, index=[1, 2, 3, 4, 8]
        )

        self.user_not_saw_this_news_df = pd.DataFrame(
            {'sport_id': [2, 3, 6],
             'adjusted_score': [0.1, 0.2, 0.2],
             'blob_id': ['lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                         'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                         'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json'],
             }, index=[1, 2, 8]
        )

        self.user_saw_this_news_df = pd.DataFrame(
                {'sport_id': [4, 3],
                 'adjusted_score': [ 0.1, 0.1],
                 'blob_id': ['lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json',
                             'lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json'],
                 }, index=[3, 4]
            )

    @pytest.fixture
    def first_setup(self):
        self.calculating_helper = MagicMock()
        self.user_preferred_teams = [1, 2, 3]
        self.user_preferred_sports = [4, 5]

    def teardown(self):
        self.app_context.pop()



    def test_user_recommendations_based_on_preferences_and_last_watch_success(self, first_setup):
        with self.app.app_context():
            user_id = 9

            self.container.news_dal().get_user_interactions_with_news_by_period_of_time.return_value = [
                MagicMock(news_id=1, blob_id='lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json', sport_id=2, save_at=datetime(2025, 3, 9, 22, 28, 23, 287946), team_index_id=1, interest_rate=1, interaction=0),
                MagicMock(news_id=2, blob_id='lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json', sport_id=3, save_at=datetime(2025, 3, 9, 22, 28, 23, 287946), team_index_id=2, interest_rate=1, interaction=0),
                MagicMock(news_id=3, blob_id='lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json', sport_id=4, save_at=datetime(2025, 3, 9, 22, 28, 23, 287946), team_index_id=3, interest_rate=1, interaction=1),
                MagicMock(news_id=4, blob_id='lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json', sport_id=3, save_at=datetime(2025, 3, 9, 22, 28, 23, 287946), team_index_id=2, interest_rate=1, interaction=1),
                MagicMock(news_id=8, blob_id='lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json', sport_id=6, save_at=datetime(2025, 3, 9, 22, 28, 23, 287946), team_index_id=3, interest_rate=1, interaction=0),
            ]

            self.container.news_dal().data_frame_to_work_with_user_and_news_data.return_value = self.user_interact_with_this_news_mask, self.user_not_interact_with_this_news_mask, self.user_and_news_details_df

            self.calculating_helper.calculate_news_coefficients_by_parameters_from_df_and_user_preferences.return_value = self.news_recommendation_coefficients_base_on_parametrs_insideDF

            self.container.news_dal().clean_duplicate_news_where_is_more_than_one_club.return_value = self.news_recommendation_coefficients_base_on_parametrs_insideDF

            self.calculating_helper.calculate_adjusted_score_by_coefficients_inside_df.return_value = self.news_with_adjusted_score_df

            self.container.news_dal().clean_duplicates_news.return_value = self.user_not_saw_this_news_df

            self.container.news_dal().assign_adjusted_scores_for_masks.return_value = self.user_saw_this_news_df, self.user_not_saw_this_news_df

            self.calculating_helper.calculate_user_average_adjusted_score_by_last_watch_news.return_value = 1

            result = self.news_service.user_recommendations_based_on_preferences_and_last_watch(
                user_id,
                self.user_preferred_teams,
                self.user_preferred_sports,
                self.calculating_helper
            )

            user_not_saw_this_news_df, recs_by_user_preferences, recs_by_user_last_watch = result

            assert recs_by_user_preferences is not None
            assert recs_by_user_last_watch is not None
            assert isinstance(user_not_saw_this_news_df, pd.DataFrame)
            assert isinstance(recs_by_user_preferences, list)
            assert isinstance(recs_by_user_last_watch, list)


    def test_user_recommendations_based_on_preferences_and_last_watch_where_user_not_watch_news(self, first_setup):
        with self.app.app_context():
            user_id = 9

            self.container.news_dal().get_user_interactions_with_news_by_period_of_time.return_value = [
                MagicMock(news_id=1, blob_id='lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json', sport_id=2, save_at=datetime(2025, 3, 9, 22, 28, 23, 287946), team_index_id=1, interest_rate=1, interaction=0),
                MagicMock(news_id=2, blob_id='lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json', sport_id=3, save_at=datetime(2025, 3, 9, 22, 28, 23, 287946), team_index_id=2, interest_rate=1, interaction=0),
                MagicMock(news_id=3, blob_id='lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json', sport_id=4, save_at=datetime(2025, 3, 9, 22, 28, 23, 287946), team_index_id=3, interest_rate=1, interaction=1),
                MagicMock(news_id=4, blob_id='lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json', sport_id=3, save_at=datetime(2025, 3, 9, 22, 28, 23, 287946), team_index_id=2, interest_rate=1, interaction=1),
                MagicMock(news_id=8, blob_id='lewis-hamilton-promises--fun-rollercoaster-ride--at-ferrari---espn.json', sport_id=6, save_at=datetime(2025, 3, 9, 22, 28, 23, 287946), team_index_id=3, interest_rate=1, interaction=0),
            ]

            self.container.news_dal().data_frame_to_work_with_user_and_news_data.return_value = self.user_interact_with_this_news_mask, self.user_not_interact_with_this_news_mask, self.user_and_news_details_df

            self.calculating_helper.calculate_news_coefficients_by_parameters_from_df_and_user_preferences.return_value = self.news_recommendation_coefficients_base_on_parametrs_insideDF

            self.container.news_dal().clean_duplicate_news_where_is_more_than_one_club.return_value = self.news_recommendation_coefficients_base_on_parametrs_insideDF

            self.calculating_helper.calculate_adjusted_score_by_coefficients_inside_df.return_value = self.news_with_adjusted_score_df

            self.container.news_dal().clean_duplicates_news.return_value = self.user_not_saw_this_news_df

            self.container.news_dal().assign_adjusted_scores_for_masks.return_value = self.user_saw_this_news_df, self.user_not_saw_this_news_df

            self.calculating_helper.calculate_user_average_adjusted_score_by_last_watch_news.return_value = -1

            result = self.news_service.user_recommendations_based_on_preferences_and_last_watch(
                user_id,
                self.user_preferred_teams,
                self.user_preferred_sports,
                self.calculating_helper
            )

            user_not_saw_this_news_df, recs_by_user_preferences, recs_by_user_last_watch = result

            assert recs_by_user_preferences is not None
            assert recs_by_user_last_watch is None
            assert isinstance(user_not_saw_this_news_df, pd.DataFrame)
            assert isinstance(recs_by_user_preferences, list)