from dependency_injector import containers, providers
from database.postgres.dal import SportDAL
from database.session import SessionLocal
from database.postgres.dal.user import UserDAL
from database.postgres.dal.preferences import PreferencesDAL
from database.postgres.dal.news import NewsDAL
from database.postgres.dal.game import GameDAL
from service.api_logic.managers.recommendation_menager import RecommendationManager
from service.api_logic.user_logic import UserService
from service.api_logic.news_logic import NewsService
from service.api_logic.games_logic import GamesService



class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.routes.api_login",
            "api.routes.api_news",
            "api.routes.api_user_preferences",
            "api.routes.api_games"
        ]
    )

    db_session = providers.Factory(SessionLocal)

    user_dal = providers.Factory(UserDAL, session=db_session)
    preferences_dal = providers.Factory(PreferencesDAL, session=db_session)
    news_dal = providers.Factory(NewsDAL, session = db_session)
    sport_dal = providers.Factory(SportDAL, db_session=db_session)

    user_service = providers.Factory(
        UserService,
        user_dal=user_dal,
        preferences_dal=preferences_dal,
        sport_dal=sport_dal,
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

    games_dal = providers.Factory(GameDAL, session=db_session)

    games_service = providers.Factory(GamesService, games_dal=games_dal)



