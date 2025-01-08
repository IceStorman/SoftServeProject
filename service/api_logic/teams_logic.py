from dto.api_input import TeamsLeagueDTO
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from database.models import TeamIndex, Sport, League, Country
from service.api_logic.scripts import apply_filters
from dto.api_output import TeamsLeagueOutput
from database.session import SessionLocal
from logger.logger import get_logger, log_function_call

api_logic_logger = get_logger("api_logic_logger", "api_logic.log")

session = SessionLocal()

# NOT WORK NOW ----------------------------------

@handle_exceptions
@log_function_call(api_logic_logger)
def get_teams(
        filters_dto: dict,
        pagination: Pagination
):
    query = (
        session.query(TeamIndex)
         .join(League, TeamIndex.league == League.league_id)
         .join(Country, TeamIndex.country == Country.country_id)
         .join(Sport, TeamIndex.sport_id == Sport.sport_id)
    )

    model_aliases = {
        "teams": TeamIndex,
        "countries": Country,
        "leagues": League,
    }

    query = apply_filters(query, filters_dto, model_aliases)

    offset, limit = pagination.get_pagination()
    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)
        api_logic_logger.info(f"Applying pagination: offset={offset}, limit={limit}")
    else:
        api_logic_logger.warning("No pagination applied. Query might return too many results or impact performance.")

    teams = query.all()
    schema = TeamsLeagueOutput(many=True)
    return schema.dump(teams)




