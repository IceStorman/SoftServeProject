import pandas as pd

from database.models import Likes, Views, News, TeamInNews, Sport, UserClubPreferences, UserPreference
from sqlalchemy import union_all, literal, func, ClauseElement
from datetime import timedelta, datetime

class NewsDAL:
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


    def get_news_by_native_id(self, news_id: str):
        return self.session.query(News).filter(News.news_id == news_id).first()


    def get_sport_by_name(self, sport_name):
        return self.session.query(Sport).filter_by(sport_name = sport_name).first()


    def get_news_native_ids_by_time_limit(self, time_limit):
        return (
            self.session.query(News.news_id)
            .filter(News.save_at >= time_limit)
            .all()
        )


    def get_user_interactions_with_news_by_period_of_time(self, user_id, period_of_time=21):
        period_of_time = datetime.now() - timedelta(days=period_of_time)

        likes_query = (
                self.session.query(
                    Likes.news_id.label('news_id'),
                    literal(4).label('interaction')
            )
            .filter(Likes.timestamp >= period_of_time, Likes.users_id == user_id)
        )

        views_query = (
                self.session.query(
                    Views.news_id.label('news_id'),
                    literal(1).label('interaction')
            )
            .filter(Views.timestamp >= period_of_time, Views.users_id == user_id)
        )

        union_query = union_all(likes_query, views_query)

        all_info_about_news_with_user_interactions_with_them = (
            self.session.query(
                News.news_id,
                News.sport_id,
                News.save_at,
                TeamInNews.team_index_id,
                func.coalesce(News.interest_rate, 1).label('interest_rate'),
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


    def data_frame_to_work_with_user_and_news_data(self, user_and_news):
        user_and_news_details_df = pd.DataFrame(
            user_and_news,
            columns=['news_id', 'sport_id', 'save_at', 'team_id', 'interest_rate_score', 'interaction_score']

        )
        user_and_news_details_df.set_index('news_id', inplace=True)

        user_interact_with_this_news_mask = user_and_news_details_df[user_and_news_details_df['interaction_score'] != 0]
        user_interact_with_this_news_mask = user_interact_with_this_news_mask[['sport_id']].copy()

        user_not_interact_with_this_news_mask = user_and_news_details_df[user_and_news_details_df['interaction_score'] == 0]
        user_not_interact_with_this_news_mask = user_not_interact_with_this_news_mask[['sport_id']].copy()

        return user_interact_with_this_news_mask, user_not_interact_with_this_news_mask, user_and_news_details_df


    def cleaning_duplicate_news_where_is_more_than_one_club(self, news_coefficients):
        news_coefficients_without_duplicates = news_coefficients.groupby('news_id').agg({
            'interest_rate_score': 'first',
            'interaction_score': 'first',
            'time_score': 'first',
            'sport_score': 'first',
            'team_score': 'sum',
        }).reset_index()

        news_coefficients_without_duplicates = news_coefficients_without_duplicates.set_index('news_id')

        return news_coefficients_without_duplicates


    def assign_adjusted_scores_for_masks(
            self,
            news_coefficients_without_duplicates,
            user_interact_with_this_news_mask,
            user_not_interact_with_this_news_mask
    ):
        user_interact_with_this_news_mask['adjusted_score'] = news_coefficients_without_duplicates['adjusted_score']
        user_not_interact_with_this_news_mask['adjusted_score'] = news_coefficients_without_duplicates['adjusted_score']
        self.delete_dataframe(news_coefficients_without_duplicates)

        return user_interact_with_this_news_mask, user_not_interact_with_this_news_mask


    def delete_dataframe(self, dataframe):
        del dataframe







