from sqlalchemy import func
from database.models import Sport, League, Country
from dto.api_output import SportsLeagueOutput, SportsOutput
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from database.session import SessionLocal
from logger.logger import Logger
from service.api_logic.filter_manager.filter_manager_factory import FilterManagerFactory

logger = Logger("logger", "all.log")

session = SessionLocal()

@handle_exceptions
@logger.log_function_call()
def get_all_sports():
    sports = session.query(Sport).all()
    schema = SportsOutput(many=True)
    return schema.dump(sports)

@handle_exceptions
@logger.log_function_call()
def search_leagues(filters_dto, pagination: Pagination):
    query = (
        session.query(League)
        .join(Sport, League.sport_id == Sport.sport_id)
        .join(Country, League.country_id == Country.country_id)
        )
   
    model_aliases = {
        "leagues": League,
        "countries": Country,
    }

    query = FilterManagerFactory.apply_filters(League, query, filters_dto, session)
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





