from dependency_injector import containers, providers
from database.postgres.dal.recommendation import RecommendationDAL
from database.session import SessionLocal
from database.postgres.dal.user import UserDAL
from service.api_logic.recommendation_logic import RecommendationService
from service.api_logic.user_logic import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.routes.api_login", "api.routes.api_news"])

    db_session = providers.Factory(SessionLocal)

    user_dal = providers.Factory(UserDAL, session=db_session)
    recommendation_dal = providers.Factory(RecommendationDAL, session=db_session)

    user_service = providers.Factory(UserService, user_dal=user_dal)
    recommendation_service = providers.Singleton(RecommendationService, recommendation_dal=recommendation_dal, user_dal=user_dal)
    fast_recommendation_service =providers.Factory(RecommendationService, recommendation_dal=recommendation_dal, user_dal=user_dal)


