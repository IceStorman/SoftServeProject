from dependency_injector import containers, providers
from database.session import SessionLocal
from service.api_logic.recommendation_logic import RecommendationService
from database.postgres.dal.recommendation import RecommendationDAL

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.routes.api_news"])

    db_session = providers.Factory(SessionLocal)

    recommendation_dal = providers.Factory(RecommendationDAL, session=db_session)

    recommendation_service = providers.Factory(RecommendationService, recommendation_dal=recommendation_dal)


