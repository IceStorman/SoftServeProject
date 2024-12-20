from typing import Dict
from database.models import Country

def extract_country(data: dict, key: str = "country") -> dict:
    if not isinstance(data, (dict, list)):
        return None

    if isinstance(data, dict):
        if key in data:
            return data[key]
        for k, v in data.items():
            result = extract_country(v, key)
            if result is not None:
                return result

    if isinstance(data, list):
        for item in data:
            result = extract_country(item, key)
            if result is not None:
                return result

    return None

def save_country(country_data: Dict, session) -> Country:
    if not country_data:
        return None

    if isinstance(country_data, str):
        country_data = {"name": country_data, "id": None, "code": None, "flag": None}

    country_api_id = country_data.get('id')
    country_name = country_data.get('name')
    country_code = country_data.get('code')
    country_flag = country_data.get('flag')

    if not country_name:
        return None

    country_entry = session.query(Country).filter_by(api_id=country_api_id).first()
    if not country_entry:
        country_entry = Country(
            api_id=country_api_id,
            name=country_name,
            code=country_code,
            flag=country_flag
        )
        session.add(country_entry)
        session.commit()

    return country_entry
