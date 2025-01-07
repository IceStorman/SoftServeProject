from dto.api_input import TeamsLeagueDTO
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from database.models import TeamIndex, Sport, League, Country
from service.api_logic.scripts import apply_filters
from dto.api_output import TeamsLeagueOutput
from database.session import SessionLocal

session = SessionLocal()

# NOT WORK NOW ----------------------------------

@handle_exceptions
def get_teams(
        filters_dto: dict,
        pagination: Pagination
):
    query = (
        session.query(TeamIndex)
         .join(League, TeamIndex.league == League.league_id)
         .join(Sport, TeamIndex.sport_id == Sport.sport_id)
    )

    model_aliases = {
        "teams": TeamIndex,
        "countries": Country,
        "leagues": League,
    }

    query = apply_filters(query, filters_dto, model_aliases)

    # offset, limit = pagination.get_pagination()
    # if offset is not None and limit is not None:
    #     query = query.offset(offset).limit(limit)

    teams = query.all()
    schema = TeamsLeagueOutput(many=True)
    return schema.dump(teams)




