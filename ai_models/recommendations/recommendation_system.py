import pandas as pd
from sqlalchemy import union_all,  literal

from database.session import SessionLocal
from datetime import datetime, timedelta
from database.models import Likes, Views, News, User, ClubPreference, UserPreference, Sport, TeamsInNews
session = SessionLocal()
from Levenshtein import ratio



# Приклад даних
# interactions = pd.DataFrame([
#     {"user_id": 1, "news_id": 101, "interaction": 5},  # Лайк
#     {"user_id": 1, "news_id": 102, "interaction": 3},  # Клік
#     {"user_id": 2, "news_id": 101, "interaction": 3},  # Клік
#     {"user_id": 2, "news_id": 103, "interaction": 5},  # Лайк
# ])
# def get_interaction_matrix():
#     time_limit = datetime.now() - timedelta(days=21)
#
#     likes_query = session.query(
#         Likes.users_id.label('user_id'),
#         Likes.news_id.label('news_id'),
#         literal(4).label('interaction'),
#         Likes.timestamp.label('timestamp')
#     ).filter(Likes.timestamp >= time_limit)
#
#     views_query = session.query(
#         Views.users_id.label('user_id'),
#         Views.news_id.label('news_id'),
#         literal(1).label('interaction'),
#         Views.timestamp.label('timestamp')
#     ).filter(Views.timestamp >= time_limit)
#
#     union_query = union_all(likes_query, views_query)
#
#     # Виконання запиту
#     interactions = session.execute(union_query).fetchall()
#
#     # Перетворення результатів на DataFrame
#     interactions_df = pd.DataFrame(interactions, columns=['user_id', 'news_id', 'interaction', 'timestamp'])
#
#     # Перетворення на матрицю
#     interaction_matrix = interactions_df.pivot_table(
#         index='user_id',
#         columns='news_id',
#         values='interaction',
#         aggfunc='sum',
#         fill_value=0
#     )
#
#     # Перевірка результату
#     print(interaction_matrix.head())
#     return interaction_matrix
#
#
# from sklearn.metrics.pairwise import cosine_similarity
#
# def user_based_recommendations(user_id, interaction_matrix, top_n=5):
#     # Обчислюємо подібність між користувачами
#     similarity_matrix = cosine_similarity(interaction_matrix)
#
#     # Індекс користувача
#     user_index = interaction_matrix.index.get_loc(user_id)
#
#     # Схожість до інших користувачів
#     user_similarity = similarity_matrix[user_index]
#
#     # Ваги для новин на основі схожих користувачів
#     weighted_scores = np.dot(user_similarity, interaction_matrix)
#
#     # Ранжуємо новини
#     recommendations = pd.Series(weighted_scores, index=interaction_matrix.columns).sort_values(ascending=False)
#
#     query = (
#         session.query(
#             ClubPreference.preferences,
#             UserPreference.sports_id
#         )
#         .join(User, UserPreference.users_id == User.user_id)
#         .join(Sport, UserPreference.sports_id == Sport.sport_id)
#         .filter_by(User.user_id == user_id)
#     )
#     user_preferences = query.all()
#
#     preferred_teams = [row.club_name for row in user_preferences]
#     preferred_sports = [row.sport_name for row in user_preferences]
#
#     # Отримуємо інформацію про новини
#     news_details = (session.query(News)
#                     .join(TeamsInNews, News.news_id == TeamsInNews.news_id)
#                     .filter(News.news_id.in_(recommendations.index.tolist())).all())
#
#     news_df = pd.DataFrame(
#         [(news.news_id, news.sport_id, team.name, news.save_at) for news, team in news_details],
#         columns=['news_id', 'sport_id', 'team_name', 'save_at']
#     )
#     news_df.set_index('news_id', inplace=True)
#
#     # Додаємо ваги за новизну
#     current_time = datetime.now()
#     news_df['time_score'] = news_df['save_at'].apply(
#         lambda t: max(0, 1 - (current_time - t).days / 21)  # Чим старіша новина, тим менше ваги
#     )
#
#     # Додаємо ваги за вподобання спорту
#     news_df['sport_score'] = news_df['sport_id'].apply(
#         lambda sport: 1.0 if sport in preferred_sports else 0.3
#     )
#
#     news_df['team_match'] = news_df['team_name'].apply(
#         lambda team: levenshtein_for_teams_similarity(team, preferred_teams)
#     )
#
#     # Призначення балів на основі результату
#     news_df['team_score'] = news_df['team_match'].apply(lambda match: 2 if match else 0)
#
#     # Об'єднуємо ваги
#     news_df['adjusted_score'] = (
#         recommendations.loc[news_df.index] *
#         news_df['time_score'] *
#         news_df['sport_score'] *
#         news_df['team_score']
#     )
#
#     # Сортуємо за новими вагами і обираємо топ N
#     final_recommendations = news_df['adjusted_score'].sort_values(ascending=False).head(top_n).index.tolist()
#     final_news = session.query(News).filter(News.news_id.in_(final_recommendations)).all()
#     return [
#         {
#             "news_id": news.news_id,
#             "score": news_df.loc[news.news_id, 'adjusted_score']
#         }
#         for news in final_news
#     ]




#
# from sklearn.metrics.pairwise import cosine_similarity
#
# # Косинусна схожість
# user_similarity = cosine_similarity(interaction_matrix)
# user_similarity = pd.DataFrame(user_similarity, index=interaction_matrix.index, columns=interaction_matrix.index)
#
#
# def recommend_news(user_id, interaction_matrix, user_similarity, top_n=5):
#     # Схожість з іншими користувачами
#     similar_users = user_similarity[user_id]
#
#     # Взаємодії інших користувачів
#     similar_users_interactions = interaction_matrix.T.dot(similar_users)
#
#     # Виключення новин, з якими користувач уже взаємодіяв
#     user_seen = interaction_matrix.loc[user_id]
#     recommendations = similar_users_interactions - user_seen
#
#     # Видача топ-N новин
#     return recommendations.sort_values(ascending=False).head(top_n)
#

def levenshtein_for_teams_similarity(team_input, team_real):
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


def get_interactions(time_limit=21):
    time_limit = datetime.now() - timedelta(days=time_limit)

    likes_query = session.query(
        Likes.users_id.label('user_id'),
        Likes.news_id.label('news_id'),
        literal(4).label('interaction'),
        Likes.timestamp.label('timestamp')
    ).filter(Likes.timestamp >= time_limit)

    views_query = session.query(
        Views.users_id.label('user_id'),
        Views.news_id.label('news_id'),
        literal(1).label('interaction'),
        Views.timestamp.label('timestamp')
    ).filter(Views.timestamp >= time_limit)

    union_query = union_all(likes_query, views_query)

    interactions = session.execute(union_query).fetchall()

    return pd.DataFrame(interactions, columns=['user_id', 'news_id', 'interaction', 'timestamp'])


def create_interaction_matrix(interactions_df):
    return interactions_df.pivot_table(
        index='user_id',
        columns='news_id',
        values='interaction',
        aggfunc='sum',
        fill_value=0
    )


def get_user_preferences(user_id):
    query = (
        session.query(
            ClubPreference.preferences,
            UserPreference.sports_id
        )
        .join(User, UserPreference.users_id == User.user_id)
        .join(Sport, UserPreference.sports_id == Sport.sport_id)
        .filter_by(User.user_id == user_id)
    )
    user_preferences = query.all()

    preferred_teams = [row.club_name for row in user_preferences]
    preferred_sports = [row.sport_name for row in user_preferences]

    return preferred_teams, preferred_sports


def get_news_details(recommendations):
    news_details = (session.query(News)
                    .join(TeamsInNews, News.news_id == TeamsInNews.news_id)
                    .filter(News.news_id.in_(recommendations.index.tolist())).all())

    news_df = pd.DataFrame(
        [(news.news_id, news.sport_id, team.name, news.save_at) for news, team in news_details],
        columns=['news_id', 'sport_id', 'team_name', 'save_at']
    )
    news_df.set_index('news_id', inplace=True)

    return news_df


def calculate_sport_score(news_sports, preferred_sports, user_interactions):
    sport_score = 0
    for sport in news_sports:
        if sport in preferred_sports:
            sport_score += 0.1
        if sport in user_interactions:
            sport_score += 0.25
    return sport_score


def get_sport_id_for_news(news_id):
    query = (
        session.query(
            Sport.sport_id
        )
        .join(Sport, Sport.sport_id == News.sport_id)
        .filter_by(News.news_id == news_id )
    )
    sport = query.all()
    return sport.sport_id if sport else None


def get_user_sport_interactions(user_id, interaction_matrix):
    # Припускаємо, що ви маєте інформацію про види спорту, з якими взаємодіє користувач
    user_interactions = set()  # Це буде набір видів спорту
    user_interaction_data = interaction_matrix.loc[user_id]

    for news_id, interaction_value in user_interaction_data.items():
        if interaction_value > 0:  # Якщо є взаємодія (лайк або перегляд)
            # Отримуємо спорт, який стосується цієї новини
            sport_id = get_sport_id_for_news(news_id)  # Потрібно визначити, як отримати sport_id для новини
            user_interactions.add(sport_id)

    return user_interactions


# def calculate_sport_score(news_sports, preferred_sports):
#     return sum(0.1 if sport in preferred_sports else 0 for sport in news_sports)


def calculate_team_score(news_teams, preferred_teams):
    return sum(0.2 if levenshtein_for_teams_similarity(team, preferred_teams) else 0 for team in news_teams)



def user_based_recommendations(user_id, interaction_matrix, top_n=5):
    preferred_teams, preferred_sports = get_user_preferences(user_id)
    user_interactions = get_user_sport_interactions(user_id, interaction_matrix)

    news_df = get_news_details(interaction_matrix)

    news_df['save_at'] = pd.to_datetime(news_df['save_at'])
    current_time = datetime.now()
    news_df['time_score'] = news_df['save_at'].apply(
        lambda t: max(0, 1 - (current_time - t).days / 21) if pd.notnull(t) else 0
    )

    news_df['sport_score'] = news_df['sport_id'].apply(
        lambda sport: calculate_sport_score([sport], preferred_sports, user_interactions)
    )

    news_df['team_score'] = news_df['team_name'].apply(
        lambda team: levenshtein_for_teams_similarity(team, preferred_teams)
    )

    news_df['adjusted_score'] = (
        interaction_matrix.loc[news_df.index] *
        news_df['time_score'] *
        news_df['sport_score'] *
        news_df['team_score']
    )

    final_recommendations = news_df['adjusted_score'].sort_values(ascending=False).head(top_n).index.tolist()

    final_news = session.query(News).filter(News.news_id.in_(final_recommendations)).all()
    return [
        {
            "news_id": news.news_id,
            "score": news_df.loc[news.news_id, 'adjusted_score']
        }
        for news in final_news
    ]


interactions_df = get_interactions()

interaction_matrix = create_interaction_matrix(interactions_df)

recommendations = user_based_recommendations(102, interaction_matrix, 5)

