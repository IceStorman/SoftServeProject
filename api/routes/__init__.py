from flask import Flask
from flask_cors import CORS
from api.routes import api_news, api_games, api_sports
from api.routes.cache import cache

# Ініціалізація додатку
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['CACHE_TYPE'] = 'SimpleCache'  # Тип кешу (наприклад, Redis)
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # За замовчуванням кеш діє 5 хвилин
    cache.init_app(app)
    app.register_blueprint(api_news.news_app, url_prefix='/news')
    app.register_blueprint(api_games.games_app, url_prefix='/games')
    app.register_blueprint(api_sports.sports_app, url_prefix='/sports')

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
