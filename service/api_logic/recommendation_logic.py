import random

from Levenshtein import ratio
from datetime import datetime, timedelta
import pandas as pd
from dto.api_input import UserInteraction, UserInteractionSchema, InputUserByIdDTO
from dto.api_output import OutputRecommendationList
from exept.exeptions import NoUsersInDBError, EmptyRecommendationListForUserError
from exept.handle_exeptions import handle_exceptions
from logger.logger import Logger

SEC_PER_DAY = 24 * 60 * 60
MAX_LIMIT_FOR_REC_IN_DAYS = 21
SCORE_FOR_NOT_PREFER_SPORT = 0.25
SCORE_FOR_PREFER_SPORT = 0.1
SCORE_FOR_PREFER_TEAM = 0.2
BASE_LIMIT_OF_NEWS_FOR_RECS = 5
MIN_PROMOTION_COF = 1
MAX_PROMOTION_COF = 4


class RecommendationService:
    def __init__(self, recommendation_dal, user_dal, news_dal):
        self._recommendation_dal = recommendation_dal
        self._user_dal = user_dal
        self._news_dal = news_dal
        self.logger = Logger("logger", "all.log").logger
        self._recommendations_list = []


    async def hybrid_recommendations(self, user=None, top_n=BASE_LIMIT_OF_NEWS_FOR_RECS):
        #if user is not None:
        if user is None:
            users_that_want_recs = self._recommendation_dal.get_all_users()
            if not users_that_want_recs:
                raise NoUsersInDBError
            interaction_df = self.__get_interactions(users_that_want_recs)
            users_interaction_matrix = self.__create_interaction_matrix(interaction_df)
            for user in users_that_want_recs:
                try:
                    recommendations_for_user_with_score = await self.__user_based_recommendations(user.user_id, users_interaction_matrix, top_n=top_n)
                    if not recommendations_for_user_with_score or not any(recommendations_for_user_with_score):
                        raise EmptyRecommendationListForUserError(user.user_id)
                    self._recommendations_list.append(recommendations_for_user_with_score)
                except EmptyRecommendationListForUserError as e:
                    self.logger.warning(f"{e}, so skipping this user")
                    continue
        else:
            interaction_df = self.__get_interactions(user)
            users_interaction_matrix = self.__create_interaction_matrix(interaction_df)
            recommendations_for_user_with_score = await self.__user_based_recommendations(user.user_id, users_interaction_matrix, top_n=top_n)
            if not recommendations_for_user_with_score or not any(recommendations_for_user_with_score):
                raise EmptyRecommendationListForUserError(user.user_id)
            self._recommendations_list.append(recommendations_for_user_with_score)
        self.logger.info("I AM HERE NOW BUT THIS SAVE NOT WORK")
        self.__save_to_db_users_recommendations(self._recommendations_list)
        self.logger.info("I AM HERE NOW SO THIS SAVE WORK NOW")

        return self._recommendations_list


    def __get_interactions(self, users_that_want_recs, time_limit=MAX_LIMIT_FOR_REC_IN_DAYS):
        time_limit = datetime.now() - timedelta(days=time_limit)
        interactions = self._recommendation_dal.get_user_interactions(time_limit)
        interactions_df = pd.DataFrame(interactions, columns=['user_id', 'news_id', 'interaction', 'timestamp'])
        interactions_grouped = interactions_df.groupby(['user_id', 'news_id'], as_index=False)['interaction'].sum()

        if isinstance(users_that_want_recs, list):
            user_ids = [user.user_id for user in users_that_want_recs]
        else:
            user_ids = [users_that_want_recs.user_id]
        all_users_df = pd.DataFrame(user_ids, columns=['user_id'])

        full_interactions = all_users_df.merge(interactions_grouped, on='user_id', how='left')
        full_interactions['news_id'] = full_interactions['news_id'].fillna(-1).astype(int)
        full_interactions['interaction'] = full_interactions['interaction'].fillna(0).astype(int)

        return full_interactions


    def __create_interaction_matrix(self, interactions_df):
        return interactions_df.pivot_table(
            index='user_id',
            columns='news_id',
            values='interaction',
            aggfunc='sum',
            fill_value=0
        )

    def __calculate_time_score(self, save_at):
        now = datetime.now()
        delta_seconds = (now - save_at).total_seconds()
        delta_days = delta_seconds / SEC_PER_DAY
        if delta_days > MAX_LIMIT_FOR_REC_IN_DAYS:
            return 0

        return 1 - (delta_days / MAX_LIMIT_FOR_REC_IN_DAYS)


    async def __user_based_recommendations(self, user_id, user_interaction_matrix, top_n=5):
        user_preferred_teams, user_preferred_sports = self.__get_user_preferences(user_id)
        user_interactions_with_sport_in_news, user_not_interactions_with_sport_in_news = self.__get_user_interactions_with_sport_in_news(user_id, user_interaction_matrix)

        news_details_df = self.__get_news_details_by_user_interaction_matrix(user_id, user_interaction_matrix)

        news_details_df['time_score'] = news_details_df['save_at'].apply(self.__calculate_time_score)

        news_details_df['sport_score'] = news_details_df['sport_id'].apply(
            lambda sport: self.__calculate_sport_score(
                [sport],
                user_preferred_sports,
                [interaction.sport_id for interaction in user_interactions_with_sport_in_news]
            )
        )

        news_details_df['team_score'] = news_details_df['team_id'].apply(
            lambda team: self.__calculate_team_score(
                [team],
                user_preferred_teams
            )
        )

        news_df_unique = news_details_df.groupby('news_id').agg({
            'sport_id': 'mean',
            'team_id': 'max',
            'save_at': 'max',
            'interest_rate_score': 'mean',
            'time_score': 'mean',
            'sport_score': 'mean',
            'team_score': 'sum',
            'interaction_score': 'max',
        }).reset_index()

        news_df_unique = news_df_unique.set_index('news_id')
        news_df_unique['adjusted_score'] = (
                news_df_unique['interest_rate_score'] *
                news_df_unique['time_score'] *
                news_df_unique['team_score'] *
                news_df_unique['sport_score']
        )

        not_seen_news, seen_news  = self.__not_seen_news(user_not_interactions_with_sport_in_news, news_df_unique)
        not_seen_news_df = news_df_unique.loc[not_seen_news]
        seen_news_df = news_df_unique.loc[seen_news]

        final_recommendations_df = not_seen_news_df['adjusted_score'].sort_values(ascending=False).head(top_n).index.tolist()

        final_news_recommendations = self._recommendation_dal.get_news_by_recommendation_list(final_recommendations_df)
        recommendations_list = [
            {
                "news_id": news.news_id,
                "score": news_df_unique.loc[news.news_id, 'adjusted_score'],
                "user_id": user_id,
                "rating": index + 1
            }
            for index, news in enumerate(final_news_recommendations)
        ]

        return OutputRecommendationList(many=True).dump(recommendations_list)


    def __get_user_preferences(self, user_id):
        user_preferences = self._recommendation_dal.get_user_preferences_by_id(user_id)

        if not user_preferences:
            return [], []

        user_preferred_teams = [row.preferences for row in user_preferences if row.preferences is not None]
        user_preferred_sports = [row.sports_id for row in user_preferences if row.sports_id is not None]

        return user_preferred_teams, user_preferred_sports


    def __get_user_interactions_with_sport_in_news(self, user_id, user_interaction_matrix):
        user_interactions = []
        user_not_interactions = []
        user_interaction_data = user_interaction_matrix.loc[user_id]

        for news_id, interaction_value in user_interaction_data.items():
            sport_id = self._recommendation_dal.get_sport_id_for_news(news_id)
            interaction = UserInteractionSchema().load(
                {
                    "sport_id": sport_id if sport_id is not None else 0,
                    "news_id": news_id if news_id != -1 else 0,
                }
            )

            if interaction_value > 0:
                user_interactions.append(interaction)
            else:
                user_not_interactions.append(interaction)

        return user_interactions, user_not_interactions


    def __get_news_details_by_user_interaction_matrix(self, user_id, user_interaction_matrix):
        news_details = self._recommendation_dal.get_news_details_by_interactions(user_interaction_matrix)

        news_details_df = pd.DataFrame(
            [
                (
                    news.news_id,
                    news.sport_id,
                    (team.team_index_id if team else 0),
                    news.save_at,
                    news.interest_rate if news.interest_rate is not None else random.uniform(MIN_PROMOTION_COF, MAX_PROMOTION_COF),
                    user_interaction_matrix.loc[user_id, news.news_id]
                ) for news, team in news_details
            ],
            columns=['news_id', 'sport_id', 'team_id', 'save_at', 'interest_rate_score', 'interaction_score']
        )
        news_details_df = news_details_df.set_index('news_id')

        return news_details_df


    def __levenshtein_for_teams_similarity(self, team_input, team_real):
        if not team_real:
            return False
        matches = []
        for preferred_team in team_real:
            similarity = ratio(team_input, preferred_team)

            if len(team_input) <= 3 and similarity == 1.0:
                matches.append(True)
            elif len(team_input) > 3 and similarity >= 0.8:
                matches.append(True)

        return any(matches)


    def __calculate_team_score(self, teams_in_news, user_preferred_teams):
        matches = sum(SCORE_FOR_PREFER_TEAM for team in teams_in_news if team in user_preferred_teams)

        return matches if matches > 0 else 0.01


    def __calculate_sport_score(self, news_sports, preferred_sports, user_interactions):
        sport_score = 0
        for sport in news_sports:
            if sport in preferred_sports:
                sport_score += SCORE_FOR_PREFER_SPORT
            if sport in user_interactions:
                sport_score += SCORE_FOR_NOT_PREFER_SPORT

        return sport_score


    def __calculate_interest_rate_score(self, news_sports, preferred_sports, user_interactions):
        sport_score = 0
        for sport in news_sports:
            if sport in preferred_sports:
                sport_score += SCORE_FOR_PREFER_SPORT
            if sport in user_interactions:
                sport_score += SCORE_FOR_NOT_PREFER_SPORT

        return sport_score


    def __not_seen_news(self, user_not_interactions_with_sport_in_news, news_df_unique):
        not_interaction_news_ids = [interaction.news_id for interaction in user_not_interactions_with_sport_in_news]
        matching_ids = news_df_unique.index.intersection(not_interaction_news_ids)
        else_ids = news_df_unique.index.difference(matching_ids)

        return matching_ids, else_ids


    def __save_to_db_users_recommendations(self, recommendations_list):
        for recs in recommendations_list:
            for user_rec in recs:
                user_id = user_rec["user_id"]
                self._recommendation_dal.save_user_recommendation(user_id, recommendations_list)


    def __send_all_info_from_blob_to_user(self, recommendations_list):
        all_news_from_blob = []
        for recs in recommendations_list:
            news_id = recs["news_id"]
            news_from_blob = self._news_dal.get_news_by_id(news_id)
            all_news_from_blob.append(news_from_blob)

        return all_news_from_blob


    async def get_recommendations_from_db(self, user_id):
        all_recs = self._recommendation_dal.get_user_recommendations(user_id)
        return OutputRecommendationList(many=True).dump(all_recs)
        # recs_for_user = self.__send_all_info_from_blob_to_user(recommendations_list)
        #
        # return recs_for_user
        # user_id = {"user_id": user_id}
        # user = InputUserByIdDTO().load(user_id)
        # q = await self.hybrid_recommendations(user)
        # return q
