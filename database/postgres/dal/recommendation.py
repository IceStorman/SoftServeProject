from database.models import Likes, Views, News, User, ClubPreference, UserPreference, Sport, TeamInNews, ActiveUser
from sqlalchemy import union_all,  literal


class RecommendationDAL:
    def __init__(self, session=None):
        self.session = session

    def get_active_users(self):
        return self.session.query(User).all()
        #self.new()
        #return [{"user_id": i} for i in range(2, 6)]  # 5 тестових юзерів

    def get_user_interactions(self, time_limit):
        try:
            likes_query = self.session.query(
                Likes.users_id.label('user_id'),
                Likes.news_id.label('news_id'),
                literal(4).label('interaction'),
                Likes.timestamp.label('timestamp')
            ).filter(Likes.timestamp >= time_limit)

            # views_query = self.session.query(
            #     Views.users_id.label('user_id'),
            #     Views.news_id.label('news_id'),
            #     literal(1).label('interaction'),
            #     Views.timestamp.label('timestamp')
            # ).filter(Views.timestamp >= time_limit)

            union_query = union_all(likes_query)

            return self.session.execute(union_query).fetchall()

        except Exception as e:
            print(e)


    def get_user_preferences_by_id(self, user_id):
        query = (
            self.session.query(
                ClubPreference.preferences,
                UserPreference.sports_id
            )
            .select_from(User)
            .outerjoin(ClubPreference, ClubPreference.users_id == User.user_id)
            .outerjoin(UserPreference, UserPreference.users_id == User.user_id)
            .filter(User.user_id == user_id)
        )

        return query.all()


    def get_sport_id_for_news(self, news_id):
        query = (
            self.session.query(
                Sport.sport_id,
                News.news_id
            )
            .join(Sport, Sport.sport_id == News.sport_id)
            .filter(News.news_id == news_id)
        )
        sport = query.all()

        return sport[0][0]  if sport else None


    def get_news_details_by_interactions(self, user_interaction_matrix):
        return  (
            self.session.query(News, TeamInNews)
            .outerjoin(TeamInNews, News.news_id == TeamInNews.news_id)
            .filter(News.news_id.in_(user_interaction_matrix.columns.tolist()))
            .all()
        )


    def get_news_by_recommendation_list(self, final_recommendations):
        return self.session.query(News).filter(News.news_id.in_(final_recommendations)).all()


    def new(self):
        from datetime import datetime
        try:
            # Тестові дані для Likes
            test_likes = [
                Likes(users_id=2, news_id=15, timestamp=datetime(2024, 1, 25)),
                Likes(users_id=2, news_id=16, timestamp=datetime(2025, 1, 27)),
                Likes(users_id=2, news_id=17, timestamp=datetime(2025, 1, 29))

            ]
            self.session.add_all(test_likes)
            self.session.commit()
        except Exception as e:
            print(e)
