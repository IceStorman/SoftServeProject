from dependency_injector import containers, providers
from database.postgres.dal import SportDAL
from database.session import SessionLocal
from database.postgres.dal.user import UserDAL
from database.postgres.dal.preferences import PreferencesDAL
from database.postgres.dal.news import NewsDAL
from database.postgres.dal.jwt import jwtDAL
from database.postgres.dal.refresh import RefreshTokenDAL 
from service.api_logic.managers.recommendation_menager import RecommendationManager
from service.api_logic.user_logic import UserService
from service.api_logic.news_logic import NewsService



class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.routes.api_login",
            "api.routes.api_news",
            "api.routes.api_user_preferences"
        ]
    )

    db_session = providers.Factory(SessionLocal)

    user_dal = providers.Factory(UserDAL, session=db_session)
    preferences_dal = providers.Factory(PreferencesDAL, session=db_session)
    news_dal = providers.Factory(NewsDAL, session = db_session)
    sport_dal = providers.Factory(SportDAL, db_session=db_session)
    jwt_dal = providers.Factory(jwtDAL, db_session = db_session)
    refresh_dal = providers.Factory(RefreshTokenDAL, db_session = db_session)

    user_service = providers.Factory(
        UserService,
        user_dal=user_dal,
        preferences_dal=preferences_dal,
        sport_dal=sport_dal,
        jwt_dal=jwt_dal,
        refresh_dal=refresh_dal
    )

    news_service = providers.Factory(
        NewsService,
        news_dal=news_dal,
        sport_dal=sport_dal,
        user_dal=user_dal,
    )

    recommendation_manager = providers.Factory(
        RecommendationManager,
        user_service,
        news_service
    )







