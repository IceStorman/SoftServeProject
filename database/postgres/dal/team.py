from sqlalchemy.orm import Session
from database.models import TeamIndex
from database.postgres.dto import TeamDTO
from typing import Optional, List
from database.postgres.dal.base import BaseDAL

class TeamDAL(BaseDAL):
    def __init__(self, session: Session):
        self.session = session

    def save_teams(self, team_dto_list : List[TeamDTO]) -> None:
        for team in team_dto_list:
            self.save_team(team)

    def save_team(self, team_dto: TeamDTO) -> int:
        team_entry = self.get_team_by_api_id_and_sport_id(team_dto.api_id, team_dto.sport_id)
        if team_entry:
            team_entry = self.update_team(team_entry.team_index_id, team_dto)
        else:
            team_entry = self.create_team(team_dto)
        return team_entry.team_index_id

    def create_team(self, team_dto: TeamDTO) -> TeamIndex:
        new_team_index = TeamIndex(
            sport_id=team_dto.sport_id,
            name=team_dto.name,
            logo=team_dto.logo,
            api_id=team_dto.api_id,
            league_id=team_dto.league
        )
        self.session.add(new_team_index)
        self.session.commit()
        self.session.refresh(new_team_index)
        return new_team_index

    def get_team_by_api_id_and_sport_id(self, team_api_id: int, team_sport_id: int):
        return self.session.query(TeamIndex).filter_by(api_id=team_api_id, sport_id=team_sport_id).first()

    def get_team_by_name_and_sport_id(self, team_name: str, team_sport_id: int):
        return self.session.query(TeamIndex).filter_by(name=team_name, sport_id=team_sport_id).first()

    def get_team_by_id(self, team_id: int) -> Optional[TeamIndex]:
        return self.session.query(TeamIndex).filter_by(team_index_id=team_id).first()

    def update_team(self, team_id: int, team_dto: TeamDTO) -> Optional[TeamIndex]:
        team_index = self.get_team_by_id(team_id)
        if not team_index:
            return None
        for field, value in team_dto.dict(exclude_unset=True).items():
            setattr(team_index, field, value)
        self.session.commit()
        self.session.refresh(team_index)
        return team_index

    def delete_team(self, team_id: int) -> bool:
        team_index = self.get_team_by_id(team_id)
        if not team_index:
            return False
        self.session.delete(team_index)
        self.session.commit()
        return True
