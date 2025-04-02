from sqlalchemy.orm import Query
from database.models import TeamIndex, Players
from service.api_logic.filter_manager.base_filter_manager import BaseFilterManager


class PlayersFilterManager(BaseFilterManager):

    @staticmethod
    def apply_sport_filter(query: Query, value: int) -> Query:
        return query.filter(Players.sport_id == value)

    @staticmethod
    def apply_name_filter(query: Query, value: str) -> Query:
        return query.filter(Players.name.ilike(f"%{value}%"))

    @staticmethod
    def apply_team_filter(query: Query, value: int) -> Query:
        return query.join(TeamIndex, Players.team_index_id == TeamIndex.team_index_id).filter(TeamIndex.api_id == value)

    FILTERS = {
        "sport_id": apply_sport_filter,
        "name": apply_name_filter,
        "team_id": apply_team_filter,
    }