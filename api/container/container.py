from dependency_injector import containers, providers
from database.session import SessionLocal
from database.postgres.dal.user import UserDAL
from database.postgres.dal.news import NewsDAL
from service.api_logic.user_logic import UserService
from service.api_logic.news_logic import NewsService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.routes.api_login"])

    db_session = providers.Factory(SessionLocal)

    user_dal = providers.Factory(UserDAL, session=db_session)

    user_service = providers.Factory(UserService, user_dal=user_dal)

    news_dal = providers.Factory(NewsDAL, session = db_session)

    news_service = providers.Factory(NewsService, news_dal=news_dal)




