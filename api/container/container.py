from dependency_injector import containers, providers
from database.session import SessionLocal
from database.postgres.dal.user import UserDAL
from database.postgres.dal.news import NewsDAL
from database.postgres.dal.recommendation import RecommendationDAL
from service.api_logic.user_logic import UserService
from service.api_logic.news_logic import NewsService
from service.api_logic.recommendation_logic import RecommendationService



class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.routes.api_login",
            "api.routes.api_news"
        ]
    )

    db_session = providers.Factory(SessionLocal)

    user_dal = providers.Factory(UserDAL, session=db_session)
    news_dal = providers.Factory(NewsDAL, session = db_session)
    recommendation_dal = providers.Factory(RecommendationDAL, session=db_session)

    user_service = providers.Factory(UserService, user_dal=user_dal)

    news_service = providers.Factory(NewsService, news_dal=news_dal)

    recommendation_service = providers.Factory(
        RecommendationService,
        recommendation_dal=recommendation_dal,
        user_dal=user_dal,
        news_dal=news_dal
    )




