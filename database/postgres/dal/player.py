from sqlalchemy.orm import Session
from database.models import Players
from database.postgres.dto import PlayerDTO
from typing import Optional, List

class PlayerDal:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_players(self, players_dto_list: List[PlayerDTO]):
        for player in players_dto_list:
            self.save_player(player)

    def save_player(self, player_dto: PlayerDTO) -> int:
        player_entry = self.get_player_by_api_id_and_sport_id(player_dto.api_id, player_dto.sport_id)
        if player_entry:
            player_entry = self.update_player(player_entry.player_id, player_dto)
        else:
            player_entry = self.create_player(player_dto)
        return player_entry.player_id

    def create_player(self, player_dto: PlayerDTO) -> Players:
        new_player = Players(
            api_id=player_dto.api_id,
            name=player_dto.name,
            logo=player_dto.logo,
            team_index_id=player_dto.team_index_id,
            sport_id=player_dto.sport_id
        )
        self.db_session.add(new_player)
        self.db_session.commit()
        self.db_session.refresh(new_player)
        return new_player

    def get_player_by_id(self, player_id: int) -> Optional[Players]:
        return self.db_session.query(Players).filter_by(player_id=player_id).first()

    def get_player_by_api_id_and_sport_id(self, player_api_id: int, player_sport_id: int):
        return self.db_session.query(Players).filter_by(api_id=player_api_id, sport_id=player_sport_id).first()

    def get_player_by_name_and_sport_id(self, player_name: str, player_sport_id: int):
        return self.db_session.query(Players).filter_by(name=player_name, sport_id=player_sport_id).first()

    def update_player(self, player_id: int, player_dto: PlayerDTO) -> Optional[Players]:
        player = self.get_player_by_id(player_id)
        if not player:
            return None
        for field, value in player_dto.dict(exclude_unset=True).items():
            setattr(player, field, value)
        self.db_session.commit()
        self.db_session.refresh(player)
        return player

    def delete_player(self, player_id: int) -> bool:
        player = self.get_player_by_id(player_id)
        if not player:
            return False
        self.db_session.delete(player)
        self.db_session.commit()
        return True
