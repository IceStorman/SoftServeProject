from sqlalchemy.orm import Session
from database.models import Country
from database.postgres.dto import CountryDTO
from typing import Optional

class CountryDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_country(self, country_dto: CountryDTO) -> int:
        country_entry = self.get_country_by_name(country_dto.name.replace("-"," "))
        if country_entry:
            country_entry = self.update_country(country_entry.country_id, country_dto)
        else:
            country_entry = self.create_country(country_dto)
        return country_entry.country_id

    def create_country(self, country_dto: CountryDTO) -> Country:
        new_country = Country(
            flag=country_dto.flag,
            name=country_dto.name,
            code=country_dto.code,
            api_id=country_dto.api_id
        )
        self.db_session.add(new_country)
        self.db_session.commit()
        self.db_session.refresh(new_country)
        return new_country

    def get_country_by_name(self, country_name: str):
        return self.db_session.query(Country).filter_by(name=country_name).first()


    def get_country_by_id(self, country_id: int) -> Optional[Country]:
        return self.db_session.query(Country).filter_by(country_id = country_id).first()

    def update_country(self, country_id: int, country_dto: CountryDTO) -> Optional[Country]:
        country = self.get_country_by_id(country_id)
        if not country:
            return None
        for field, value in country_dto.dict(exclude_unset=True).items():
            setattr(country, field, value)
        self.db_session.commit()
        self.db_session.refresh(country)
        return country

    def delete_country(self, country_id: int) -> bool:
        country = self.get_country_by_id(country_id)
        if not country:
            return False
        self.db_session.delete(country)
        self.db_session.commit()
        return True
