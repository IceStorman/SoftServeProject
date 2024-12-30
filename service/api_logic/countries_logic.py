from requests import session
from sqlalchemy import func
from database.models import Country
from dto.api_output import CountriesOutput
from exept.handle_exeptions import handle_exceptions
from database.session import SessionLocal

session = SessionLocal()

@handle_exceptions
def get_countries():
    countries = session.query(Country).all()
    schema = CountriesOutput(many=True)
    return schema.dump(countries)



@handle_exceptions
def search_countries(query):
    countries = session.query(Country).filter(
        func.lower(Country.name).like(f"{query}%")
    ).all()
    schema = CountriesOutput(many=True)
    return schema.dump(countries)
