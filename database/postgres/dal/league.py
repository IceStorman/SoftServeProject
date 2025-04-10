from sqlalchemy.orm import Session
from database.models import League
from database.postgres.dto import LeagueDTO
from typing import Optional, List
from database.postgres.dal.base import BaseDAL

class LeagueDAL(BaseDAL):
    def __init__(self, session: Session):
        self.session = session

    def save_leagues(self, league_dto_list: List[LeagueDTO]):
        for league in league_dto_list:
            self.save_league(league)

    def save_league(self, league_dto: LeagueDTO) -> int:
        league_entry = self.get_league_by_api_id_and_sport_id(league_dto.api_id, league_dto.sport_id)
        if league_entry:
            league_entry = self.update_league(league_entry.league_id, league_dto)
        else:
            league_entry = self.create_league(league_dto)
        return league_entry.league_id

    def create_league(self, league_dto: LeagueDTO) -> League:
        new_league = League(
            api_id=league_dto.api_id,
            name=league_dto.name,
            logo=league_dto.logo,
            sport_id=league_dto.sport_id,
            country_id=league_dto.country
        )
        self.session.add(new_league)
        self.session.commit()
        self.session.refresh(new_league)
        return new_league

    def get_league_by_id(self, league_id: int) -> Optional[League]:
        return self.session.query(League).filter_by(league_id=league_id).first()

    def get_league_by_api_id_and_sport_id(self, league_api_id: int, league_sport_id: int):
        return self.session.query(League).filter_by(api_id=league_api_id, sport_id=league_sport_id).first()

    def get_league_by_name_and_sport_id(self, league_name: str, league_sport_id: int):
        return self.session.query(League).filter_by(name=league_name, sport_id=league_sport_id).first()


    def update_league(self, league_id: int, league_dto: LeagueDTO) -> Optional[League]:
        league = self.get_league_by_id(league_id)
        if not league:
            return None
        for field, value in league_dto.dict(exclude_unset=True).items():
            setattr(league, field, value)
        self.session.commit()
        self.session.refresh(league)
        return league

    def delete_league(self, league_id: int) -> bool:
        league = self.get_league_by_id(league_id)
        if not league:
            return False
        self.session.delete(league)
        self.session.commit()
        return True
