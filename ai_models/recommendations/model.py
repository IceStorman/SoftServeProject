import lightgbm as lgb
import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, jsonify, request
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from imblearn.over_sampling import SMOTE
from database.models import *
from database.session import SessionLocal
from service.implementation.auto_request_api.logic_request_by_react import result

SessionLocal = SessionLocal()
app = Flask(__name__)

# Глобальна змінна для моделі
model = None
train_data = None

# Налаштування параметрів для LightGBM
params = {
    'objective': 'binary',
    'metric': 'binary_logloss',
    'boosting_type': 'gbdt',
    'learning_rate': 0.1,
    'num_leaves': 31,
    'min_data_in_leaf': 1,  # Можна зменшити це значення
    'min_data_in_bin': 1,
    'is_unbalance': True  # Add this parameter to handle class imbalance

}


def load_initial_data():
    """Завантажити всі доступні дані для первинного навчання."""
    interactions = SessionLocal.query(
        Interaction.user_id,
        Interaction.news_id,
        Interaction.interaction_type,
        News.sport_id,
        News.team_name,
        News.interest_rate,
        News.save_at,
        ClubPreference.preferences,
        UserPreference.sports_id
    ).join(News, Interaction.news_id == News.news_id) \
     .join(User, Interaction.user_id == User.user_id) \
     .join(ClubPreference, User.user_id == ClubPreference.users_id) \
     .join(UserPreference, User.user_id == UserPreference.users_id) \
     .join(Sport, UserPreference.sports_id == Sport.sport_id)
    results = interactions.all()
    SessionLocal.close()

    data = [
        {
            "user_id": r.user_id,
            "news_id": r.news_id,
            "interaction_type": r.interaction_type,
            "sport_name_n": r.sport_id,
            "team_name_n": r.team_name,
            "interest_rate": r.interest_rate,
            "save_at": r.save_at,
            "team_name": r.team_name,
            "sport_name": r.sport_name,
        }
        for r in results
    ]
    df = pd.DataFrame(data)
    print(f"Number of rows retrieved: {len(df)}")
    return df


def check_team_match(row):
    teams = row['teams'] if isinstance(row['teams'], list) else row['teams'].split(",")
    team_name = row['team_name'] if isinstance(row['team_name'], list) else row['team_name'].split(",")

    return 1 if any(team in team_name for team in teams) else 0


def check_sport_match(row):
    sport = row['sport'] if isinstance(row['sport'], list) else row['sport'].split(",")
    sport_name = row['sport_name'] if isinstance(row['sport_name'], list) else row['sport_name'].split(",")

    return 1 if any(s in sport_name for s in sport) else 0


def prepare_features(data):
    """ Підготовка фіч для моделі """
    print(f"Data before feature preparation: {len(data)} rows")

    data['publication_date'] = pd.to_datetime(data['save_at'])
    data['days_since_pub'] = (datetime.datetime.now() - data['save_at']).dt.days
    data['team_match'] = data.apply(check_team_match, axis=1)
    data['sport_match'] = data.apply(check_sport_match, axis=1)
    data['interaction_type'] = data['interaction_type'].apply(lambda x: 1 if x == 'click' else 0)

    print(f"Data after feature preparation: {len(data)} rows")

    features = data[['team_match', 'sport_match', 'popularity', 'days_since_pub']]
    return features


def train_initial_model():
    """ Первинне навчання моделі """
    global train_data, model
    data = load_initial_data()
    X = prepare_features(data)
    y = data['interaction_type']

    # Перевірка на дисбаланс класів
    print(f"Class distribution before balancing: \n{y.value_counts()}")

    # Якщо є дисбаланс класів, використовуємо SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    print(f"Class distribution after balancing: \n{y_resampled.value_counts()}")

    # Створення об'єкта Dataset для LightGBM
    train_data = lgb.Dataset(X_resampled, label=y_resampled)
    model = lgb.train(params, train_data)
    return model

def update_model():
    """Оновлення моделі на основі нових взаємодій за останні 2 години."""
    two_hours_ago = datetime.datetime.now() - datetime.timedelta(hours=2)

    new_interactions = SessionLocal.query(
        Interaction.user_id,
        Interaction.news_id,
        Interaction.interaction_type,
        News.blob_id,
        News.interest_rate,
        News.save_at,
        ClubPreference.preferences.label('team_name'),
        Sport.sport_name
    ).join(News, Interaction.news_id == News.news_id) \
     .join(User, Interaction.user_id == User.user_id) \
     .join(ClubPreference, User.user_id == ClubPreference.users_id) \
     .join(UserPreference, User.user_id == UserPreference.users_id) \
     .join(Sport, UserPreference.sports_id == Sport.sport_id) \
     .filter(News.save_at >= two_hours_ago).all()
    SessionLocal.close()

    if new_interactions:
        data = [{
            "user_id": i.user_id,
            "news_id": i.news_id,
            "interaction_type": i.interaction_type,
            "blob_id": i.blob_id,
            "interest_rate": i.interest_rate,
            "save_at": i.save_at,
            "team_name": i.team_name,
            "sport_name": i.sport_name
        } for i in new_interactions]

        df = pd.DataFrame(data)
        X_new = prepare_features(df)
        y_new = df['interaction_type']
        new_data_set = lgb.Dataset(X_new, label=y_new, reference=train_data)

        global model
        model = lgb.train(params, new_data_set, init_model=model, keep_training_booster=True)


def recommend_news(user_id, model):
    """Генерація рекомендацій для конкретного користувача."""
    # Отримати переваги по командам
    user_teams = SessionLocal.query(ClubPreference.preferences).filter_by(users_id=user_id).all()
    user_teams = [team.preferences for team in user_teams]
    SessionLocal.close()

    # Отримати переваги по видам спорту
    user_sports = SessionLocal.query(Sport.sport_name) \
        .join(UserPreference, Sport.sport_id == UserPreference.sports_id) \
        .filter(UserPreference.users_id == user_id).all()
    user_sports = [sport.sport_name for sport in user_sports]
    SessionLocal.close()

    # Отримати доступні новини
    news_data = SessionLocal.query(
        News.news_id,
        News.blob_id,
        News.interest_rate,
        News.save_at
    ).all()
    SessionLocal.close()

    news_df = pd.DataFrame([{
        "news_id": n.news_id,
        "blob_id": n.blob_id,
        "interest_rate": n.interest_rate,
        "save_at": n.save_at
    } for n in news_data])

    # Додати фічі для команди та спорту
    news_df['team_match'] = news_df['blob_id'].apply(lambda x: 1 if x in user_teams else 0)
    news_df['sport_match'] = news_df['blob_id'].apply(lambda x: 1 if x in user_sports else 0)
    news_df['days_since_save'] = (datetime.datetime.now() - news_df['save_at']).dt.days

    # Передбачення моделі
    X_news = news_df[['team_match', 'sport_match', 'interest_rate', 'days_since_save']]
    news_df['score'] = model.predict(X_news)

    recommendations = news_df.sort_values(by='score', ascending=False).head(10)
    return recommendations[['news_id', 'score']].to_dict(orient='records')


@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    """ API для отримання рекомендацій """
    user_id = request.args.get("user_id", type=int)
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    recommendations = recommend_news(user_id, model)
    return jsonify({"recommendations": recommendations})


@app.route('/initialize_model', methods=['POST'])
def initialize_model_endpoint():
    """ Ініціалізація моделі при запуску додатку """
    global model
    model = train_initial_model()
    return jsonify({"status": "model initialized"}), 200


# Налаштування планувальника для оновлення моделі кожні 2 години
scheduler = BackgroundScheduler()
scheduler.add_job(update_model, 'interval', hours=2)
scheduler.start()

# Запуск Flask
if __name__ == "__main__":
    model = train_initial_model()  # Початкове навчання
    app.run(debug=True)
