from sqlalchemy import func
from database.models import Sport, League, Country
from dto.api_output import SportsLeagueOutput, SportsOutput
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from service.api_logic.scripts import apply_filters
from database.session import SessionLocal
from logger.logger import get_logger, log_function_call

api_logic_logger = get_logger("api_logic_logger", "api_logic.log")

session = SessionLocal()

@handle_exceptions
@log_function_call(api_logic_logger)
def get_all_sports():
    sports = session.query(Sport).all()
    schema = SportsOutput(many=True)
    return schema.dump(sports)


@handle_exceptions
@log_function_call(api_logic_logger)
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
        api_logic_logger.info(f"Applying pagination: offset={offset}, limit={limit}")
    else:
        api_logic_logger.warning("No pagination applied. Query might return too many results or impact performance.")

    leagues = query.all()
    count = len(leagues)
    schema = SportsLeagueOutput(many=True)
    leagues = schema.dump(leagues)
    return  {
        "count": count,
        "leagues": leagues,
    }


@handle_exceptions
@log_function_call(api_logic_logger)
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
        api_logic_logger.info(f"Applying pagination: offset={offset}, limit={limit}")
    else:
        api_logic_logger.warning("No pagination applied. Query might return too many results or impact performance.")

    countries = query.all()

    schema = SportsLeagueOutput(many=True)
    leagues = schema.dump(countries)
    return {
        "count": count,
        "leagues": leagues,
    }





