from dto.api_input import TeamsLeagueDTO
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from database.models import TeamIndex, Sport, League, Country
from service.api_logic.scripts import apply_filters
from dto.api_output import TeamsLeagueOutput
from database.session import SessionLocal
from sqlalchemy import func


session = SessionLocal()

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
    print("--------"*3)
    a = query.all()
    print("--------"*3)

    # for p in a:
    #     print(f"ID: {p.api_id}, Name: {p.name}, League: {p.logo}, Sport ID: {p.sport_id}")


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
    teams = schema.dump(teams)
    return {
        "count": count,
        "teams": teams,
    }




