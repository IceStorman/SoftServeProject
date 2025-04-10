from random import random
import random
import pandas as pd
from database.models import News, TeamInNews, Sport, InteractionWithNews
from sqlalchemy import union_all, literal, func, ClauseElement, case
from datetime import timedelta, datetime
from database.postgres.dal.base import BaseDAL
from service.api_logic.helpers.calculating_helper import RecommendationConsts


PERIOD_OF_TIME = 90

class NewsDAL(BaseDAL):
    def __init__(self, session = None):
        self.session = session


    def fetch_news(self, order_by=None, limit=None, filters=None):
        query = self.session.query(News)
        
        if filters:
            query = query.filter(*filters)
        
        if order_by is not None:
            if isinstance(order_by, ClauseElement):  
                query = query.order_by(order_by)
            else:
                raise ValueError("Invalid order_by argument. Must be a SQLAlchemy ClauseElement.")
        
        if limit:
            query = query.limit(limit)
        
        return query.all()


    def get_news_by_id(self, blob_id: str):
        return self.session.query(News).filter(News.blob_id == blob_id).first()

    def get_news_by_native_id(self, news_ids):
        return self.session.query(News).filter(News.news_id.in_(news_ids)).all()


    def get_news_native_ids_by_time_limit(self, time_limit):
        return (
            self.session.query(News.news_id)
            .filter(News.save_at >= time_limit)
            .all()
        )


    def get_user_interactions_with_news_by_period_of_time(self, user_id: int, period_of_time: int = PERIOD_OF_TIME) -> list[tuple]:
        period_of_time = datetime.now() - timedelta(days=period_of_time)

        likes_query = (
                self.session.query(
                    InteractionWithNews.news_id.label('news_id'),
                    literal(4).label('interaction')
            )
            .filter(InteractionWithNews.timestamp >= period_of_time, InteractionWithNews.user_id == user_id, InteractionWithNews.interaction_id == 1)

        )

        views_query = (
                self.session.query(
                    InteractionWithNews.news_id.label('news_id'),
                    literal(1).label('interaction')
            )

            .filter(InteractionWithNews.timestamp >= period_of_time, InteractionWithNews.user_id == user_id, InteractionWithNews.interaction_id == 4)
        )

        union_query = union_all(likes_query, views_query)

        all_info_about_news_with_user_interactions_with_them = (
            self.session.query(
                News.news_id,
                News.blob_id,
                News.sport_id,
                News.save_at,
                TeamInNews.team_index_id,
                func.coalesce(case(
            (News.likes == 0, 1),
                    else_=News.likes ), 1),
                func.coalesce(union_query.c.interaction, 0).label('interaction')
            )
            .select_from(News)
            .join(union_query, News.news_id == union_query.c.news_id, isouter=True
        )
        .outerjoin(TeamInNews, News.news_id == TeamInNews.news_id))

        all_info_about_news_by_period_of_time_with_user_interactions_with_them = (
            all_info_about_news_with_user_interactions_with_them
            .filter(
                News.save_at >= period_of_time
            )
        )

        return list(set(all_info_about_news_by_period_of_time_with_user_interactions_with_them.all()))


    def data_frame_to_work_with_user_and_news_data(self, user_and_news: list[tuple]) -> pd.DataFrame.mask and pd.DataFrame.mask and pd.DataFrame:
        user_and_news_details_df = pd.DataFrame(
            user_and_news,
            columns=['news_id', 'blob_id', 'sport_id', 'save_at', 'team_id', 'interest_rate_score', 'interaction_score']

        )
        user_and_news_details_df.set_index('news_id', inplace=True)

        user_interact_with_this_news_mask = user_and_news_details_df[user_and_news_details_df['interaction_score'] != 0]
        user_interact_with_this_news_mask = user_interact_with_this_news_mask[['sport_id']].copy()

        user_not_interact_with_this_news_mask = user_and_news_details_df[user_and_news_details_df['interaction_score'] == 0]
        user_not_interact_with_this_news_mask = user_not_interact_with_this_news_mask[['sport_id']].copy()

        return user_interact_with_this_news_mask, user_not_interact_with_this_news_mask, user_and_news_details_df


    def clean_duplicate_news_where_is_more_than_one_club(self, news_coefficients: pd.DataFrame) -> pd.DataFrame:

        def process_team_score(group):
            if (group != 0.1).any():
                return group[group != 0.1].sum()
            else:
                return group.iloc[0]

        news_coefficients_without_duplicates = news_coefficients.groupby('news_id').agg({
            'blob_id': 'first',
            'interest_rate_score': 'first',
            'interaction_score': 'first',
            'time_score': 'first',
            'sport_score': 'first',
            'team_score': process_team_score,
        }).reset_index()

        news_coefficients_without_duplicates = news_coefficients_without_duplicates.set_index('news_id')

        return news_coefficients_without_duplicates


    def clean_duplicates_news(self, news_df: pd.DataFrame) -> pd.DataFrame:
        news_df_without_duplicates = news_df.groupby('news_id').agg({
            'sport_id': 'first',
        }).reset_index()
        news_df_without_duplicates = news_df_without_duplicates.set_index('news_id')

        return news_df_without_duplicates


    def assign_adjusted_scores_for_masks(
            self,
            news_coefficients_without_duplicates: pd.DataFrame,
            user_interact_with_this_news_mask: pd.DataFrame.mask,
            user_not_interact_with_this_news_mask: pd.DataFrame.mask,
    ) -> pd.DataFrame.mask and pd.DataFrame.mask:

        if not user_interact_with_this_news_mask.empty:
            user_interact_with_this_news_mask[['adjusted_score', 'blob_id']] = news_coefficients_without_duplicates[['adjusted_score', 'blob_id']]
        user_not_interact_with_this_news_mask[['adjusted_score','blob_id']] = news_coefficients_without_duplicates[['adjusted_score','blob_id']]
        self.delete_dataframe(news_coefficients_without_duplicates)

        return user_interact_with_this_news_mask, user_not_interact_with_this_news_mask


    def delete_dataframe(self, dataframe):
        del dataframe







