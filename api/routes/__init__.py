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
    api_user_preferences
)
from api.routes.cache import cache
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from database.session import DATABASE_URL
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from dotenv import load_dotenv


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
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=3)
    jwt.init_app(app)

    app.config['GOOGLE_CLIENT_ID'] = os.getenv('GOOGLE_CLIENT_ID')
    app.config['GOOGLE_CLIENT_SECRET'] = os.getenv('GOOGLE_CLIENT_SECRET')
    app.config['REDIRECT_URI'] = 'http://127.0.0.1:5001/login/auth/google/callback'
    app.config['AUTHORIZATION_BASE_URL'] = 'https://accounts.google.com/o/oauth2/auth'
    app.config['TOKEN_URL'] = 'https://oauth2.googleapis.com/token'
    app.config['USER_INFO_URL'] = 'https://www.googleapis.com/oauth2/v2/userinfo'
    app.config['SCOPES'] = 'https://www.googleapis.com/auth/userinfo.email'

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
    app.register_blueprint(api_login.login_app, url_prefix='/login')


    app.container = Container()

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, use_reloader=False)

