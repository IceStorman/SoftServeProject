from flask import Flask, jsonify
from flask_cors import CORS
from api.container.container import Container
from api.routes import (
    api_news,
    api_games,
    api_sports,
    api_teams,
    api_countries,
    api_login,
    api_interactions,
    api_user_preferences,
    api_streams,
    api_localization,
    api_user_preferences,
    api_comments
)
from api.routes.api_login import login_app
from api.routes.api_sports import sports_app
from api.routes.api_news import news_app
from api.routes.api_streams import streams_app
from api.routes.api_games import games_app
from api.routes.api_countries import countries_app
from api.routes.cache import cache
from api.routes.api_localization import babel, get_locale
from api.routes.localization_compilling import LocalizationCompiler
from flask_swagger_ui import get_swaggerui_blueprint
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from database.session import DATABASE_URL
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv
from pathlib import Path
from api.routes.api_localization import babel, get_locale


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
cert_file = os.path.join(BASE_DIR, "localhost.pem")
key_file = os.path.join(BASE_DIR, "localhost-key.pem")

load_dotenv()
db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()


def create_app():
    app = Flask(__name__, static_folder='static')
    CORS(app, supports_credentials=True)

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['JSON_AS_ASCII'] = False
    app.config['CACHE_DEFAULT_TIMEOUT'] = 60*5
    cache.init_app(app)

    app.secret_key = os.getenv('SECRET_KEY')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FRONTEND_NEWS_URL'] = os.getenv('FRONTEND_NEWS_URL')
    mail.init_app(app)
    
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt.init_app(app)

    app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
    app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
    app.config['REDIRECT_URI'] = os.getenv('GOOGLE_REDIRECT_URI')
    app.config['AUTHORIZATION_BASE_URL'] = os.getenv('GOOGLE_AUTHORIZATION_BASE_URL')
    app.config['TOKEN_URL'] = os.getenv('GOOGLE_TOKEN_URL')
    app.config['USER_INFO_URL'] = os.getenv('GOOGLE_USER_INFO_URL')
    app.config['SCOPES'] = os.getenv('GOOGLE_SCOPES')

    BASE_DIR = Path(__file__).resolve().parent
    TRANSLATIONS_DIR = BASE_DIR / 'translations'
    app.config['BABEL_DEFAULT_LOCALE'] = 'en'
    app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'uk']
    app.config['BABEL_TRANSLATION_DIRECTORIES'] = str(TRANSLATIONS_DIR)
    babel.init_app(app, locale_selector=get_locale)

    app.config["API_TITLE"] = "QSPORT API"
    app.config["API_VERSION"] = "1.0"
    app.config["OPENAPI_VERSION"] = "3.0.2"

    app.register_blueprint(api_teams.teams_app, url_prefix='/teams')
    app.register_blueprint(api_interactions.interactions_app, url_prefix='/interactions')
    app.register_blueprint(api_localization.localization_app, url_prefix='/')
    app.register_blueprint(api_user_preferences.preferences_app, url_prefix='/preferences')
    app.register_blueprint(api_comments.comments_app, url_prefix='/comments')


    app.container = Container()

    return app


def create_swagger_documentation():
    api = Api(app)

    SWAGGER_URL = '/swagger'
    API_URL = '/openapi.json'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "QSPORT API",
        },
    )

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
    api.register_blueprint(login_app)
    api.register_blueprint(sports_app)
    api.register_blueprint(news_app)
    api.register_blueprint(streams_app)
    api.register_blueprint(games_app)
    api.register_blueprint(countries_app)


    @app.route('/openapi.json')
    def openapi_spec():
        return jsonify(api.spec.to_dict())


app = create_app()

if __name__ == '__main__':
    LocalizationCompiler().compile_translations()
    create_swagger_documentation()
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False, ssl_context=(cert_file, key_file))


