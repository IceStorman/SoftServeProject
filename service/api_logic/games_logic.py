from dto.api_output import GameOutput
from dto.api_input import GamesDTO
from database.models import Games, Country, TeamIndex, League, Sport
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from service.api_logic.scripts import apply_filters
from sqlalchemy.orm import aliased
from database.session import SessionLocal
from logger.logger import get_logger, log_function_call

api_logic_logger = get_logger("api_logic_logger", "api_logic.log")

session = SessionLocal()

@handle_exceptions
@log_function_call(api_logic_logger)
def get_games_today(
        filters_dto: dict,
        pagination: Pagination
):
    home_team = aliased(TeamIndex)
    away_team = aliased(TeamIndex)

    query = (
        session.query(
            Games,
            League.name.label("league_name"),
            League.logo.label("league_logo"),
            Country.name.label("country_name"),
            home_team.name.label("home_team_name"),
            home_team.logo.label("home_team_logo"),
            away_team.name.label("away_team_name"),
            away_team.logo.label("away_team_logo"),
        )
        .join(League, Games.league_id == League.league_id)
        .join(Country, Games.country_id == Country.country_id)
        .join(Sport, Games.sport_id == Sport.sport_id)
        .join(home_team, Games.team_home_id == home_team.team_index_id)
        .join(away_team, Games.team_away_id == away_team.team_index_id)
    )

    model_aliases = {
        "games": Games,
        "countries": Country,
        "leagues": League,
    }

    query = apply_filters(query, filters_dto, model_aliases)

    offset, limit = pagination.get_pagination()
    if offset is not None and limit is not None:
        api_logic_logger.info(f"Applying pagination: offset={offset}, limit={limit}")
        query = query.offset(offset).limit(limit)
    else:
        api_logic_logger.warning("No pagination applied. Query might return too many results or impact performance.")

    games = query.all()
    schema = GameOutput(many=True)
    return schema.dump(games)


