from dependency_injector import containers, providers
from database.postgres.dal import SportDAL, LeagueDAL
from database.session import SessionLocal
from database.postgres.dal.user import UserDAL
from database.postgres.dal.preferences import PreferencesDAL
from database.postgres.dal.news import NewsDAL
from database.postgres.dal.game import GameDAL
from database.postgres.dal.team import TeamDAL
from database.postgres.dal.access_token import AccessTokensDAL
from database.postgres.dal.refresh import RefreshTokenDAL 
from service.api_logic.managers.recommendation_menager import RecommendationManager
from service.api_logic.sports_logic import SportService
from service.api_logic.user_logic import UserService
from service.api_logic.news_logic import NewsService
from service.api_logic.games_logic import GamesService
from service.api_logic.teams_logic import TeamsService
from api.refresh_token_logic import UserInfoService



class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.routes.api_login",
            "api.routes.api_news",
            "api.routes.api_user_preferences",
            "api.routes.api_games",
            "api.routes.api_teams",
            "api.routes.api_sports",
        ]
    )

    db_session = providers.Factory(SessionLocal)

    user_dal = providers.Factory(UserDAL, session=db_session)
    preferences_dal = providers.Factory(PreferencesDAL, session=db_session)
    news_dal = providers.Factory(NewsDAL, session = db_session)
    sport_dal = providers.Factory(SportDAL, session=db_session)
    games_dal = providers.Factory(GameDAL, session=db_session)
    teams_dal = providers.Factory(TeamDAL, session=db_session)
    leagues_dal = providers.Factory(LeagueDAL, session=db_session)
    access_tokens_dal = providers.Factory(AccessTokensDAL, db_session = db_session)
    refresh_dal = providers.Factory(RefreshTokenDAL, db_session = db_session)

    games_service = providers.Factory(GamesService, games_dal=games_dal)
    teams_service = providers.Factory(TeamsService, teams_dal=teams_dal)
    sports_service = providers.Factory(SportService, sports_dal=sport_dal, leagues_dal=leagues_dal)
    
    user_service = providers.Factory(
        UserService,
        user_dal=user_dal,
        preferences_dal=preferences_dal,
        sport_dal=sport_dal,
        access_tokens_dal=access_tokens_dal,
        refresh_dal=refresh_dal,
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
        news_service,
        user_dal=user_dal,
    )