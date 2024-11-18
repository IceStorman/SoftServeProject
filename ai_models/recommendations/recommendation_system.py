from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import sched, time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mac:D100406m@localhost/postgres'
db = SQLAlchemy(app)


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    popularity = db.Column(db.Integer, default=0)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    favorite_sport = db.Column(db.String(50))
    favorite_team = db.Column(db.String(50))


class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    score = db.Column(db.Integer)


def fetch_latest_news():
    latest_news = News.query.order_by(News.created_at.desc()).limit(10).all()
    football_news = News.query.filter_by(category='football').order_by(News.created_at.desc()).limit(10).all()
    basketball_news = News.query.filter_by(category='basketball').order_by(News.created_at.desc()).limit(10).all()
    volleyball_news = News.query.filter_by(category='volleyball').order_by(News.created_at.desc()).limit(10).all()
    hockey_news = News.query.filter_by(category='hockey').order_by(News.created_at.desc()).limit(10).all()
    popular_news = News.query.order_by(News.popularity.desc()).limit(10).all()

    return {
        "latest": [news.title for news in latest_news],
        "football": [news.title for news in football_news],
        "basketball": [news.title for news in basketball_news],
        "volleyball": [news.title for news in volleyball_news],
        "hockey": [news.title for news in hockey_news],
        "popular": [news.title for news in popular_news],
    }


from datetime import datetime, timedelta

def recommend_news_for_user(user):
    user_preferences = {
        'sport': user.favorite_sport,
        'team': user.favorite_team
    }

    recommendations = []
    all_news = News.query.all()

    print(f"User Preferences: {user_preferences}")
    print(f"Total News Articles: {len(all_news)}")

    for news in all_news:
        score = 0
        if user_preferences['sport'] in news.category:
            score += 4
            print(f"Score for sport match in {news.title}: +3")
        if user_preferences['team'] in news.title:
            score += 2
            print(f"Score for team match in {news.title}: +1")

        # Calculate recency score (assuming 0-5, 5 being the newest)
        recency_score = 5 - (datetime.now() - news.created_at).days  # Adjust according to your logic
        recency_score = max(recency_score, 0)  # Ensure it doesn't go below 0
        score += recency_score
        print(f"Recency Score for {news.title}: {recency_score}")

        if score > 0:
            recommendations.append((news, score))
            print(f"Added to recommendations: {news.title} with score {score}")

    # Sort by score (descending) and take the top 5
    recommendations.sort(key=lambda x: x[1], reverse=True)

    print("Top Recommendations with Scores:")
    for news, score in recommendations[:5]:
        print(f"{news.title}: Score = {score}")

    return [news[0].title for news in recommendations[:5]]


@app.route('/recommendations/<int:user_id>', methods=['GET'])
def get_recommendations(user_id):
    user = Users.query.get(user_id)
    if user:
        recommended_news = recommend_news_for_user(user)
        return jsonify(recommended_news)
    return jsonify({"message": "User not found."}), 404

@app.route('/')
def home():
    return "Welcome to the AI Recommendation System!"

@app.route('/test')
def test():
    return jsonify({"status": "success", "message": "The server is running!"})

if __name__ == '__main__':
    # Запускаємо періодичний запит
    scheduler = sched.scheduler(time.time, time.sleep)


    def periodic_fetch():
        news_data = fetch_latest_news()
        print(news_data)
        scheduler.enter(1800, 1, periodic_fetch)  # 30 хвилин


    scheduler.enter(0, 1, periodic_fetch)
    app.run(debug=True)
