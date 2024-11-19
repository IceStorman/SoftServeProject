from flask import Flask
from api.routes import api_news, api_games, api_sports

# Ініціалізація додатку
def create_app():
    app = Flask(__name__)

    app.register_blueprint(api_news.news_app, url_prefix='/news')
    app.register_blueprint(api_games.games_app, url_prefix='/games')
    app.register_blueprint(api_sports.sports_app, url_prefix='/sports')

    return app



app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
