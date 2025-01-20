from dto.api_input import TeamsLeagueDTO
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from database.models import TeamIndex, Sport, League, Country
from service.api_logic.scripts import apply_filters
from dto.api_output import TeamsLeagueOutput
from database.session import SessionLocal
from logger.logger import Logger
from sqlalchemy import func

api_logic_logger = Logger("api_logic_logger", "api_logic_logger.log")

session = SessionLocal()

# NOT WORK NOW ----------------------------------

@handle_exceptions
@api_logic_logger.log_function_call()
def get_teams(
        filters_dto: dict,
        pagination: Pagination
):
    query = (
        session.query(TeamIndex)
         .join(League, TeamIndex.league == League.league_id)
         .join(Sport, TeamIndex.sport_id == Sport.sport_id)
         # .filter(
         #    func.lower(TeamIndex.name)
         #    .like(f"{filters_dto.get('letter', '')}%")
         # )
    )

    model_aliases = {
        "teams": TeamIndex,
        "leagues": League,
    }

    query = apply_filters(query, filters_dto, model_aliases)
    count = query.count()

    offset, limit = pagination.get_pagination()
    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)

    teams = query.all()
    schema = TeamsLeagueOutput(many=True)
    team = schema.dump(teams)
    return {
        "count": count,
        "teams": team,
    }



