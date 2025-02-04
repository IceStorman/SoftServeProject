from sqlalchemy.orm import aliased

from database.models import Likes, Views, News, User, ClubPreference, UserPreference, Sport, TeamInNews, \
    UserRecommendations
from sqlalchemy import union_all, literal, func


class RecommendationDAL:
    def __init__(self, session=None):
        self.session = session


    def get_all_users(self):
        return self.session.query(User).all()


    def get_user_interactions(self, time_limit):
        likes_query = self.session.query(
            Likes.users_id.label('user_id'),
            Likes.news_id.label('news_id'),
            literal(4).label('interaction'),
            Likes.timestamp.label('timestamp')
        ).filter(Likes.timestamp >= time_limit)

        views_query = self.session.query(
            Views.users_id.label('user_id'),
            Views.news_id.label('news_id'),
            literal(1).label('interaction'),
            Views.timestamp.label('timestamp')
        ).filter(Views.timestamp >= time_limit)

        union_query = union_all(likes_query, views_query)
        # aliased_union = aliased(union_query)
        #
        # aggregated_query = (
        #     self.session.query(
        #         aliased_union.c.user_id,
        #         aliased_union.c.news_id,
        #         func.sum(aliased_union.c.interaction).label('interaction')
        #     )
        #     .group_by(aliased_union.c.user_id, aliased_union.c.news_id)
        # )

        return self.session.execute(union_query).fetchall()


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


    # def save_user_recommendation(self, user_id, recommendations):
    #     self.session.query(UserRecommendations).filter_by(user_id=user_id).delete()
    #
    #     recommendation_objects = [
    #         UserRecommendations(
    #             user_id=rec['user_id'],
    #             news_id=rec['news_id'],
    #             score=rec['score'],
    #             rating=rec['rating'],
    #         )
    #         for rec in recommendations
    #     ]
    #     self.session.add_all(recommendation_objects)
    #     self.session.commit()

    def save_user_recommendation(self, user_id, recommendations):
        existing_recommendations = (
            self.session.query(UserRecommendations)
            .filter_by(user_id=user_id)
            .all()
        )

        num_existing = len(existing_recommendations)
        num_new = len(recommendations)

        for i in range(min(num_existing, num_new)):
            existing_recommendations[i].news_id = recommendations[i]['news_id']
            existing_recommendations[i].score = recommendations[i]['score']
            existing_recommendations[i].rating = recommendations[i]['rating']

        if num_new > num_existing:
            new_records = [
                UserRecommendations(
                    user_id=user_id,
                    news_id=rec['news_id'],
                    score=rec['score'],
                    rating=rec['rating']
                )
                for rec in recommendations[num_existing:]
            ]
            self.session.add_all(new_records)

        elif num_new < num_existing:
            for i in range(num_new, num_existing):
                existing_recommendations[i].news_id = -1
                existing_recommendations[i].score = 0
                existing_recommendations[i].rating = 0

        self.session.commit()


    def get_user_recommendations(self, user_id):
        return self.session.query(UserRecommendations).filter_by(user_id=user_id).all()
        # return [
        #     {
        #         "news_id": 13,
        #         "score": 0.143415255,
        #         "user_id": 2
        #     }
        # ]


    def new(self):
        from datetime import datetime
        test_likes = [
            Likes(users_id=2, news_id=31, timestamp=datetime(2024, 1, 25)),
            Likes(users_id=2, news_id=32, timestamp=datetime(2025, 1, 27)),
            Likes(users_id=3, news_id=33, timestamp=datetime(2025, 1, 31))
        ]
        self.session.add_all(test_likes)
        self.session.commit()

