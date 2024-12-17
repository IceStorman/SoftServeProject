from flask import Flask
from flask_cors import CORS
from api.routes import api_news, api_games, api_sports, api_teams
from api.routes.cache import cache

# Ініціалізація додатку
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['JSON_AS_ASCII'] = False
    app.config['CACHE_DEFAULT_TIMEOUT'] = 60*5
    cache.init_app(app)
    app.register_blueprint(api_news.news_app, url_prefix='/news')
    app.register_blueprint(api_games.games_app, url_prefix='/games')
    app.register_blueprint(api_sports.sports_app, url_prefix='/sports')
    app.register_blueprint(api_teams.teams_app, url_prefix='/team')


    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

