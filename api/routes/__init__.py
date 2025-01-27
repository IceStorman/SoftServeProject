import os
from flask import Flask
from flask_cors import CORS
from api.container.container import Container
from api.routes import api_news, api_games, api_sports, api_teams, api_countries, api_login
from api.routes.cache import cache
from flask_swagger_ui import get_swaggerui_blueprint
from flask_sqlalchemy import SQLAlchemy
from database.session import DATABASE_URL
from flask_mail import Mail
from flask_jwt_extended import JWTManager, create_access_token
from itsdangerous import URLSafeTimedSerializer, BadSignature
from datetime import timedelta



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

    app.secret_key = "SECRET_KEY"
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = 'q.sport.news@gmail.com'
    app.config['MAIL_PASSWORD'] = 'jjrc siyp trnq tzcp'
    mail.init_app(app)
    
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=3)
    jwt.init_app(app)

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

