from dependency_injector import containers, providers
from database.postgres.dal.user_subscription import UserSubscriptionDAL
from database.postgres.dal import SportDAL, LeagueDAL, PlayerDal
from database.session import SessionLocal
from database.postgres.dal.user import UserDAL
from database.postgres.dal.preferences import PreferencesDAL
from database.postgres.dal.news import NewsDAL
from database.postgres.dal.game import GameDAL
from database.postgres.dal.team import TeamDAL
from database.postgres.dal.access_token import AccessTokensDAL
from database.postgres.dal.refresh import RefreshTokenDAL
from database.postgres.dal.comment import CommentDAL
from service.api_logic.managers.recommendation_menager import RecommendationManager
from service.api_logic.player_logic import PlayerService
from service.api_logic.sports_logic import SportService
from service.api_logic.user_logic import UserService
from service.api_logic.news_logic import NewsService
from service.implementation.email_sender.user_subscription_manager import UserSubscriptionManager
from database.postgres.dal import StreamDAL
from service.api_logic.streams_logic import StreamService
from service.api_logic.games_logic import GamesService
from service.api_logic.teams_logic import TeamsService
from service.api_logic.comments_logic import CommentsService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.routes.api_login",
            "api.routes.api_news",
            "api.routes.api_user_preferences",
            "api.routes.api_streams",
            "api.routes.api_games",
            "api.routes.api_teams",
            "api.routes.api_sports",
            "service.implementation.email_sender.user_subscription_manager",
            "api.routes.api_comments",
        ]
    )

    db_session = providers.Factory(SessionLocal)

    user_dal = providers.Factory(UserDAL, session=db_session)
    preferences_dal = providers.Factory(PreferencesDAL, session=db_session)
    news_dal = providers.Factory(NewsDAL, session = db_session)
    user_subscription_dal = providers.Factory(UserSubscriptionDAL, session=db_session)
    stream_dal = providers.Factory(StreamDAL, session = db_session)
    sport_dal = providers.Factory(SportDAL, session=db_session)
    games_dal = providers.Factory(GameDAL, session=db_session)
    teams_dal = providers.Factory(TeamDAL, session=db_session)
    leagues_dal = providers.Factory(LeagueDAL, session=db_session)
    access_tokens_dal = providers.Factory(AccessTokensDAL, db_session = db_session)
    refresh_dal = providers.Factory(RefreshTokenDAL, db_session = db_session)
    players_dal = providers.Factory(PlayerDal, session = db_session)
    comments_dal = providers.Factory(CommentDAL, session=db_session)

    games_service = providers.Factory(GamesService, games_dal=games_dal)
    teams_service = providers.Factory(TeamsService, teams_dal=teams_dal)
    sports_service = providers.Factory(SportService, sports_dal=sport_dal, leagues_dal=leagues_dal)

    stream_service = providers.Factory(
        StreamService,
        stream_dal = stream_dal
    )

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

    email_manager = providers.Factory(
        UserSubscriptionManager,
        user_subscription_dal,
        preferences_dal
    )
    players_service = providers.Factory(
        PlayerService,
        players_dal=players_dal
    )

    comments_service = providers.Factory(
        CommentsService,
        comments_dal=comments_dal,
        news_dal=news_dal
    )
