from sqlalchemy.orm import Session
from database.models import Games
from database.postgres.dto import GameDTO
from typing import Optional, List
from database.postgres.dal.base import BaseDAL

class GameDAL(BaseDAL):
    def __init__(self, session: Session):
        self.session = session

    def save_games(self, game_dto_list: List[GameDTO]):
        for game in game_dto_list:
            self.save_game(game)


    def save_game(self, game_dto: GameDTO) -> int:
        game_entry = self.get_game_by_game_id_and_api_id(game_dto.game_id, game_dto.api_id)
        if game_entry:
            game_entry = self.update_game(game_dto.game_id, game_dto)
        else:
            game_entry = self.create_game(game_dto)
        return game_entry.game_id

    def create_game(self, games_dto: GameDTO) -> Games:
        new_game = Games(
            league_id=games_dto.league_id,
            sport_id=games_dto.sport_id,
            country_id=games_dto.country_id,
            team_away_id=games_dto.team_away_id,
            team_home_id=games_dto.team_home_id,
            score_away_team=games_dto.score_away_team,
            score_home_team=games_dto.score_home_team,
            status=games_dto.status,
            type=games_dto.game_status,
            time=games_dto.time,
            date=games_dto.date,
            api_id=games_dto.api_id
        )

        self.session.add(new_game)
        self.session.commit()
        self.session.refresh(new_game)
        
        return new_game

    def get_game_by_game_id_and_api_id(self, game_id: int, game_api_id: int) -> Optional[Games]:
        return self.session.query(Games).filter_by(game_id = game_id, api_id=game_api_id).first()

    def get_game_by_id(self, game_id: int) -> Optional[Games]:
        return self.session.query(Games).filter_by(game_id = game_id).first()

    def update_game(self, game_id: int, games_dto: GameDTO) -> Optional[Games]:
        game = self.get_game_by_id(game_id)
        if not game:
            return None
        for field, value in games_dto.dict(exclude_unset=True).items():
            setattr(game, field, value)
        self.session.commit()
        self.session.refresh(game)

        return game

    def delete_game(self, game_id: int) -> bool:
        game = self.get_game_by_id(game_id)
        if not game:
            return False

        self.session.delete(game)
        self.session.commit()

        return True
