from dependency_injector import containers, providers
from database.session import SessionLocal
from database.postgres.dal.user import UserDAL
from database.postgres.dal.preferences import PreferencesDAL
from service.api_logic.login_logic import UserService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.routes.api_login", "api.routes.api_user_preferences"])

    db_session = providers.Factory(SessionLocal)

    user_dal = providers.Factory(UserDAL, session=db_session)
    preferences_dal = providers.Factory(PreferencesDAL, session=db_session)

    user_service = providers.Factory(UserService, user_dal=user_dal, preferences_dal=preferences_dal)


