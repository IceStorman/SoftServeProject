from sqlalchemy import func
from database.models import Sport, League, Country
from dto.api_input import SearchDTO, SportsLeagueDTO
from dto.api_output import SportsLeagueOutputDTO, SportsOutputDTO
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

    model_aliases = {
        "leagues": League,
    }

    query = apply_filters(query, filters_dto.to_dict(), model_aliases)

    offset, limit = filters_dto.get_pagination()
    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)

    leagues = query.all()
    count = query.count()

    return [
        SportsLeagueOutputDTO(
            id=league.league_id,
            sport=league.sport_id,
            logo=league.logo,
            name=league.name,
            count=count,
        ).to_dict() for league in leagues
    ]


@handle_exceptions
def search_leagues(session, filters_dto: SearchDTO):
    query = (
        session.query(League)
        .join(Sport, League.sport_id == Sport.sport_id)
        .join(Country, League.country == Country.country_id)
        .filter(
            func.lower(League.name)
            .like(f"{filters_dto.letter}%")
        )
    )
   
    model_aliases = {
        "leagues": League,
        "countries": Country,
    }

    query = apply_filters(query, filters_dto.to_dict(), model_aliases)
    count = query.count()

    offset, limit = filters_dto.get_pagination()
    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)

    countries = query.all()

    return [
        SportsLeagueOutputDTO(
            id=country.league_id,
            sport=country.sport_id,
            logo=country.logo,
            name=country.name,
            count=count,
        ).to_dict() for country in countries
    ]





