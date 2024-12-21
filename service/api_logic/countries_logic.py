from database.models import Country
from dto.api_output import CountriesOutputDTO
from exept.handle_exeptions import handle_exceptions


@handle_exceptions
def get_countries(session):
    countries = session.query(Country).all()
    return [
        CountriesOutputDTO(
            id=country.api_id,
            flag=country.flag,
            name=country.name,
        ).to_dict() for country in countries
    ]
