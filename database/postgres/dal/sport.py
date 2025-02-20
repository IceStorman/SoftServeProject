from sqlalchemy.orm import Session
from database.models import Sport
from database.postgres.dto import SportDTO
from typing import Optional
from dto.api_output import SportsOutput


class SportDAL:
    def __init__(self, db_session = None):
        self.db_session = db_session

    def create_sport(self, sport_dto: SportDTO) -> Sport:
        new_sport = Sport(
            sport_name=sport_dto.sport_name,
            sport_img=sport_dto.sport_img
        )
        self.db_session.add(new_sport)
        self.db_session.commit()
        self.db_session.refresh(new_sport)
        return new_sport

    def get_sport_by_name(self, sport_name: str) -> Optional[Sport]:
        return self.db_session.query(Sport).filter_by(sport_name = sport_name).first()

    def get_sport_by_id(self, sport_id: int) -> Optional[Sport]:
        return self.db_session.query(Sport).filter_by(sport_id = sport_id).first()

    def update_sport(self, sport_id: int, sport_dto: SportDTO) -> Optional[Sport]:
        sport = self.get_sport_by_id(sport_id)
        if not sport:
            return None
        for field, value in sport_dto.dict(exclude_unset=True).items():
            setattr(sport, field, value)
        self.db_session.commit()
        self.db_session.refresh(sport)
        return sport

    def delete_sport(self, sport_id: int) -> bool:
        sport = self.get_sport_by_id(sport_id)
        if not sport:
            return False
        self.db_session.delete(sport)
        self.db_session.commit()
        return True

    def get_query(self):
        return self.db_session.query(Sport)

    def execute_query(self, query):
        return query.all()