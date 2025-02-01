from dependency_injector import containers, providers
from database.session import SessionLocal
from database.postgres.dal.user import UserDAL
from service.api_logic.user_logic import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.routes.api_login"])

    db_session = providers.Factory(SessionLocal)

    user_dal = providers.Factory(UserDAL, session=db_session)

    user_service = providers.Factory(UserService, user_dal=user_dal)


