from nltk.sem.chat80 import country

from database.models import Sport, League
from api.routes.dto import SportsLeagueDTO, SportsLeagueOutputDTO, SportsOutputDTO
from exept.handle_exeptions import handle_exceptions
from service.api_logic.scripts import apply_filters


@handle_exceptions
def get_all_sports(session):
    sports = session.query(Sport).all()
    return [
        SportsOutputDTO(
            id=sport.sport_id,
            sport=sport.sport_name,
            logo=sport.sport_img,
        ).to_dict() for sport in sports
    ]


@handle_exceptions
def get_all_leagues_by_sport(session, filters_dto: SportsLeagueDTO):
    query = (
        session.query(
            League.sport_id,
            League.league_id,
            League.logo,
            League.name,
            League.country,
            League.api_id
        )
        .join(Sport, League.sport_id == Sport.sport_id)
    )
    count = get_leagues_count_by_sport(session, filters_dto.sport_id)

    model_aliases = {
        "leagues": League,
    }

    query = apply_filters(query, filters_dto.to_dict(), model_aliases)

    offset, limit = filters_dto.get_pagination()

    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)

    leagues = query.all()

    return [
        SportsLeagueOutputDTO(
            id=league.league_id,
            sport=league.sport_id,
            logo=league.logo,
            name=league.name,
            count=count,
        ).to_dict() for league in leagues
    ]

def get_leagues_count_by_sport(session, sport_id):
    count = session.query(League).join(Sport, League.sport_id == Sport.sport_id).filter(League.sport_id == sport_id).count()
    return count