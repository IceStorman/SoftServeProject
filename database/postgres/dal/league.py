from sqlalchemy.orm import Session
from database.models import League
from database.postgres.dto import LeagueDTO
from typing import Optional, List

class LeagueDAL:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_leagues(self, league_dto_list: List[LeagueDTO]):
        for league in league_dto_list:
            self.save_league(league)

    def save_league(self, league_dto: LeagueDTO):
        league_entry = self.get_league_by_api_id_and_sport_id(league_dto.api_id, league_dto.sport_id)
        if league_entry:
            self.update_league(league_entry.league_id, league_dto)
        else:
            self.create_league(league_dto)

    def create_league(self, league_dto: LeagueDTO) -> League:
        new_league = League(
            api_id=league_dto.api_id,
            name=league_dto.name,
            logo=league_dto.logo,
            sport_id=league_dto.sport_id,
            country=league_dto.country
        )
        self.db_session.add(new_league)
        self.db_session.commit()
        self.db_session.refresh(new_league)
        return new_league

    def get_league_by_id(self, league_id: int) -> Optional[League]:
        return self.db_session.query(League).filter_by(league_id=league_id).first()

    def get_league_by_api_id_and_sport_id(self, league_api_id: int, league_sport_id: int):
        return self.db_session.query(League).filter_by(api_id=league_api_id, sport_id=league_sport_id).first()

    def get_league_by_name_and_sport_id(self, league_name: str, league_sport_id: int):
        return self.db_session.query(League).filter_by(name=league_name, sport_id=league_sport_id).first()


    def update_league(self, league_id: int, league_dto: LeagueDTO) -> Optional[League]:
        league = self.get_league_by_id(league_id)
        if not league:
            return None
        for field, value in league_dto.dict(exclude_unset=True).items():
            setattr(league, field, value)
        self.db_session.commit()
        self.db_session.refresh(league)
        return league

    def delete_league(self, league_id: int) -> bool:
        league = self.get_league_by_id(league_id)
        if not league:
            return False
        self.db_session.delete(league)
        self.db_session.commit()
        return True
