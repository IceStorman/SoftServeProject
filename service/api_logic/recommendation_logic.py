import asyncio
from keras.src.losses import cosine_similarity
from Levenshtein import ratio
from datetime import datetime, timedelta
import pandas as pd

class UserInteraction:
    def __init__(self, sport_id, news_id):
        self.sport_id = sport_id
        self.news_id = news_id

class RecommendationService:
    def __init__(self, recommendation_dal):
        self._recommendation_dal = recommendation_dal
        #self.logger = Logger("api_logic_logger", "api_logic_logger.log").logger

    def recommendations(self):
        users = self._recommendation_dal.get_active_users()

        tasks = []
        for user in users:
            #if not user.is_expired():
                task = asyncio.create_task(self.process_user_recommendations(user))
                tasks.append(task)

        asyncio.gather(*tasks)

    def process_user_recommendations(self, user):
        user_id = user["user_id"]
        recommendations = self.hybrid_recommendations(user_id)
        # send_recommendations(user.user_id, recommendations)
        socketio.emit("recommendations", {"user_id": user_id, "data": recommendations})

    def hybrid_recommendations(self, user_id, alpha=0.6, beta=0.3, top_n=5):
        try:
            interaction_df = self.get_interactions()
            #not_interaction_df = self.get_not_interactions()
            interaction_matrix = self.create_interaction_matrix(interaction_df)

            content_scores = self.user_based_recommendations(user_id, interaction_matrix, top_n=top_n)
            cf_scores = self.get_cf_recommendations(user_id, interaction_matrix, top_n=top_n)

            final_scores = {}

            for news in set(content_scores + cf_scores):
                final_scores[news] = (
                        alpha * (content_scores.get(news, 0)) +
                        beta * (cf_scores.get(news, 0))
                )

            return sorted(final_scores, key=final_scores.get, reverse=True)[:top_n]
        except Exception as e:
            print(e)

    def get_interactions(self, time_limit=21):
        time_limit = datetime.now() - timedelta(days=time_limit)
        interactions = self._recommendation_dal.get_user_interactions(time_limit)
        interactions_df = pd.DataFrame(interactions, columns=['user_id', 'news_id', 'interaction', 'timestamp'])
        interactions_df = interactions_df.groupby(['user_id', 'news_id'], as_index=False)['interaction'].sum()
        print(interactions_df)

        return interactions_df

    def get_not_interactions(self, time_limit=21):
        time_limit = datetime.now() - timedelta(days=time_limit)
        interactions = self._recommendation_dal.get_user_interactions(time_limit)
        interactions_df = pd.DataFrame(interactions, columns=['user_id', 'news_id', 'interaction', 'timestamp'])
        interactions_df = interactions_df.groupby(['user_id', 'news_id'], as_index=False)['interaction'].sum()
        print(interactions_df)

        return interactions_df

    def create_interaction_matrix(self, interactions_df):
        print(interactions_df.shape)
        print(interactions_df.head())
        print(interactions_df)
        return interactions_df.pivot_table(
            index='user_id',
            columns='news_id',
            values='interaction',
            aggfunc='sum',
            fill_value=0
        )


    def user_based_recommendations(self, user_id, user_interaction_matrix, top_n=5):
        user_preferred_teams, user_preferred_sports = self.get_user_preferences(user_id)
        user_interactions_with_sport_in_news, user_not_interactions_with_sport_in_news = self.get_user_sport_interactions(user_id, user_interaction_matrix)

        news_df = self.get_news_details_by_user_interaction_matrix(user_id, user_interaction_matrix)


        news_df['save_at'] = pd.to_datetime(news_df['save_at'])
        current_time = datetime.now()
        news_df['time_score'] = news_df['save_at'].apply(
            lambda t: max(0, 1 - (current_time - t).days / 21) if pd.notnull(t) else 0
        )

        news_df['sport_score'] = news_df['sport_id'].apply(
            lambda sport: self.calculate_sport_score(
                [sport],
                user_preferred_sports,
                [interaction.sport_id for interaction in user_interactions_with_sport_in_news]
            )
        )

        news_df['team_score'] = news_df['team_name'].apply(
            lambda team: self.calculate_team_score(
                [team],
                user_preferred_teams
            )
        )

        news_df_unique = news_df.groupby('news_id').agg({
            'sport_id': 'mean',
            'team_name': 'max',
            'save_at': 'max',
            'time_score': 'mean',
            'sport_score': 'mean',
            'team_score': 'sum'
        }).reset_index()
        news_df_unique = news_df_unique.set_index('news_id')

        news_df_unique['adjusted_score'] = news_df_unique['sport_score'] * news_df_unique['time_score'] + news_df_unique['team_score']
        # print(news_df_unique.dtypes)
        # print(news_df.dtypes)
        # news_df_unique['save_at'] = (news_df_unique['save_at'] - pd.Timestamp("1970-01-01")) // pd.Timedelta(
        #     '1s')
        #
        # print(news_df_unique.dtypes)
        # print(news_df.dtypes)
        #
        # adjusted_scorerrr = (
        #         news_df_unique.loc[news_df_unique.index] *
        #         news_df_unique['time_score'] *
        #         news_df_unique['sport_score'] *
        #         news_df_unique['team_score']
        # )
        # news_df_unique['adjusted_scorerrr'] = adjusted_scorerrr

        matching_ids, else_ids  = self.not_seen_news(user_not_interactions_with_sport_in_news, news_df_unique)
        not_seen_news_df = news_df_unique.loc[matching_ids]
        seen_news_df = news_df_unique.loc[else_ids]

        final_recommendations = not_seen_news_df['adjusted_score'].sort_values(ascending=False).head(top_n).index.tolist()

        final_news = self._recommendation_dal.get_news_by_recommendation_list(final_recommendations)
        return [
            {
                "news_id": news.news_id,
                "score": news_df_unique.loc[news.news_id, 'adjusted_score']
            }
            for news in final_news
        ]

    # def get_user_preferences(self, user_id):
    #     user_preferences = self._recommendation_dal.get_user_preferences_by_id(user_id)
    #
    #     preferred_teams = [row.preferences for row in user_preferences]
    #     preferred_sports = [row.sport_id for row in user_preferences]
    #
    #     return preferred_teams, preferred_sports
    def get_user_preferences(self, user_id):
        user_preferences = self._recommendation_dal.get_user_preferences_by_id(user_id)

        if not user_preferences:
            return [], []

        preferred_teams = [row[0] for row in user_preferences if row[0] is not None]
        preferred_sports = [row[1] for row in user_preferences if row[1] is not None]

        return preferred_teams, preferred_sports

    def get_user_sport_interactions(self, user_id, interaction_matrix):
        user_interactions = []
        user_not_interactions = []
        user_interaction_data = interaction_matrix.loc[user_id]

        for news_id, interaction_value in user_interaction_data.items():
            sport_id = self._recommendation_dal.get_sport_id_for_news(news_id)
            interaction = UserInteraction(sport_id, news_id)

            if interaction_value > 0:
                user_interactions.append(interaction)
            else:
                user_not_interactions.append(interaction)

        return user_interactions, user_not_interactions

    def get_news_details_by_user_interaction_matrix(self, user_id, user_interaction_matrix):
        news_details = self._recommendation_dal.get_news_details_by_interactions(user_interaction_matrix)

        news_df = pd.DataFrame(
            [(news.news_id, news.sport_id, (team.team_index_id if team else 0), news.save_at, user_interaction_matrix.loc[user_id, news.news_id]) for news, team in news_details],
            columns=['news_id', 'sport_id', 'team_name', 'save_at', 'interaction_score']
        )
        news_df = news_df.set_index('news_id')

        return news_df


    def levenshtein_for_teams_similarity(self, team_input, team_real):
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

    def calculate_sport_score(self, news_sports, preferred_sports, user_interactions):
        sport_score = 0
        for sport in news_sports:
            if sport in preferred_sports:
                sport_score += 0.1
            if sport in user_interactions:
                sport_score += 0.25
        return sport_score

    def not_seen_news(self, user_not_interactions_with_sport_in_news, news_df_unique):
        not_interaction_news_ids = [interaction.news_id for interaction in user_not_interactions_with_sport_in_news]
        matching_ids = news_df_unique.index.intersection(not_interaction_news_ids)
        else_ids = news_df_unique.index.difference(matching_ids)
        return matching_ids, else_ids

    def calculate_team_score(self, news_teams, preferred_teams):
        return sum(0.2 if self.levenshtein_for_teams_similarity(team, preferred_teams) else 0 for team in news_teams)

    def get_cf_recommendations(self, user_id, interaction_matrix, top_n=5):
        similar_users = self.get_similar_users(user_id, interaction_matrix)
        similar_users_interactions = interaction_matrix.loc[similar_users].mean()

        return similar_users_interactions.sort_values(ascending=False).head(top_n).index.tolist()

    def get_similar_users(self, user_id, interaction_matrix, top_n=5):
        if user_id not in interaction_matrix.index:
            return []

        # Вираховуємо схожість користувача з іншими
        similarity_matrix = cosine_similarity(interaction_matrix, interaction_matrix)
        user_index = interaction_matrix.index.get_loc(user_id)
        print(user_index)

        # Беремо top_n найсхожіших користувачів (окрім самого себе)
        similar_users = sorted(
            list(enumerate(similarity_matrix[user_index, :])),
            key=lambda x: x[1], reverse=True
        )[1:top_n + 1]  # Пропускаємо самого себе

        return [interaction_matrix.index[i] for i, _ in similar_users]


