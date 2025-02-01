from service.api_logic.websocket import socketio
from flask import Flask
from flask_cors import CORS
from api.routes import api_news, api_games, api_sports, api_teams, api_countries
from api.routes.cache import cache
from flask_swagger_ui import get_swaggerui_blueprint
from api.container.container import Container



def create_app():
    app = Flask(__name__, static_folder='static')
    CORS(app)
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['JSON_AS_ASCII'] = False
    app.config['CACHE_DEFAULT_TIMEOUT'] = 60*5
    cache.init_app(app)
    socketio.init_app(app)

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Test application"
        },
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    app.register_blueprint(api_news.news_app, url_prefix='/news')
    app.register_blueprint(api_games.games_app, url_prefix='/games')
    app.register_blueprint(api_sports.sports_app, url_prefix='/sports')
    app.register_blueprint(api_teams.teams_app, url_prefix='/teams')
    app.register_blueprint(api_countries.countries_app, url_prefix='/countries')

    app.container = Container()



    return app


app = create_app()
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True, use_reloader=False, allow_unsafe_werkzeug=True)

