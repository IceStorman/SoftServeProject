from sqlalchemy import func
from database.models import Sport, League, Country
from dto.api_output import SportsLeagueOutput, SportsOutput
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from service.api_logic.scripts import apply_filters
from database.session import SessionLocal

session = SessionLocal()

@handle_exceptions
def get_all_sports():
    sports = session.query(Sport).all()
    schema = SportsOutput(many=True)
    return schema.dump(sports)


@handle_exceptions
def get_all_leagues_by_sport(filters_dto: dict, pagination: Pagination):
    query = (
        session.query(League)
        .join(Sport, League.sport_id == Sport.sport_id)
    )

    model_aliases = {
        "leagues": League,
    }

    query = apply_filters(query, filters_dto, model_aliases)

    offset, limit = pagination.get_pagination()
    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)

    leagues = query.all()
    count = len(leagues)
    schema = SportsLeagueOutput(many=True)
    leagues = schema.dump(leagues)
    return  {
        "count": count,
        "leagues": leagues,
    }


@handle_exceptions
def search_leagues(filters_dto: dict, pagination: Pagination):
    query = (
        session.query(League)
        .join(Sport, League.sport_id == Sport.sport_id)
        .join(Country, League.country == Country.country_id)
        .filter(
            func.lower(League.name)
            .like(f"{filters_dto.get('letter', '')}%")
        )
    )
   
    model_aliases = {
        "leagues": League,
        "countries": Country,
    }

    query = apply_filters(query, filters_dto, model_aliases)
    count = query.count()

    offset, limit = pagination.get_pagination()
    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)

    countries = query.all()

    schema = SportsLeagueOutput(many=True)
    leagues = schema.dump(countries)
    return {
        "count": count,
        "leagues": leagues,
    }





