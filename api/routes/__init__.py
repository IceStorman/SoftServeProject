import subprocess

from flask import Flask
from flask_cors import CORS
from api.container.container import Container
from api.routes import (
    api_news,
    api_games,
    api_sports,
    api_teams,
    api_countries,
    api_login,
    api_user_preferences,
    api_streams,
    api_localization
)
from api.routes.api_localization import get_locale
from api.routes.api_login import login_app
from api.routes.cache import cache
from api.routes.api_localization import babel
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from database.session import DATABASE_URL
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()



def create_app():
    app = Flask(__name__, static_folder='static')
    CORS(app)

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
    mail.init_app(app)
    
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False
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
    app.register_blueprint(api_streams.streams_app, url_prefix='/streams')
    app.register_blueprint(api_localization.localization_app, url_prefix='/')
    app.register_blueprint(api_login.login_app, url_prefix='/user')
    app.register_blueprint(api_user_preferences.preferences_app, url_prefix='/preferences')


    app.container = Container()

    return app


def compile_translations():
    BASE_DIR = Path(__file__).resolve().parent
    TRANSLATIONS_DIR = BASE_DIR / 'translations'
    subprocess.run(["pybabel", "compile", "-d", str(TRANSLATIONS_DIR)], check=True)



app = create_app()
if __name__ == '__main__':
    compile_translations()
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)

