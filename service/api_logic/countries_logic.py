from requests import session
from sqlalchemy import func
from database.models import Country
from dto.api_output import CountriesOutput
from exept.handle_exeptions import handle_exceptions
from database.session import SessionLocal
from logger.logger import get_logger, log_function_call

api_logic_logger = get_logger("api_logic_logger", "api_logic.log")

session = SessionLocal()

@handle_exceptions
@log_function_call(api_logic_logger)
def get_countries():
    countries = session.query(Country).all()
    schema = CountriesOutput(many=True)
    return schema.dump(countries)


@handle_exceptions
@log_function_call(api_logic_logger)
def search_countries(query):
    countries = session.query(Country).filter(
        func.lower(Country.name).like(f"{query}%")
    ).all()
    schema = CountriesOutput(many=True)
    return schema.dump(countries)
