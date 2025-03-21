from dto.api_output import GameOutput, ListResponseDTO
from dto.api_input import GamesDTO
from database.models import Games, Country, TeamIndex, League, Sport
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from sqlalchemy.orm import aliased
from logger.logger import Logger
from service.api_logic.filter_manager.filter_manager_strategy import FilterManagerStrategy

class GamesService:
    def __init__(self, games_dal):
        self._games_dal = games_dal
        self._logger = Logger("logger", "all.log").logger

    def get_games_today(self, filters_dto: GamesDTO()):
        AwayTeam = aliased(TeamIndex)
        HomeTeam = aliased(TeamIndex)

        query = (self._games_dal.get_base_query(Games).with_entities(
            Games.status,
            Games.date,
            Games.time,
            Games.sport_id,
            Games.score_away_team,
            Games.score_home_team,
            League.name.label("league_name"),
            League.logo.label("league_logo"),
            HomeTeam.name.label("home_team_name"),
            HomeTeam.logo.label("home_team_logo"),
            AwayTeam.name.label("away_team_name"),
            AwayTeam.logo.label("away_team_logo"),
        )
        .join(League, Games.league_id == League.league_id)
        .join(AwayTeam, Games.team_away_id == AwayTeam.team_index_id)
        .join(HomeTeam, Games.team_home_id == HomeTeam.team_index_id)
    )

        filtered_query, count = FilterManagerStrategy.apply_filters(Games, query, filters_dto)

        games = self._games_dal.query_output(filtered_query)
        game_output = GameOutput(many=True)
        games = game_output.dump(games)

        response_dto = ListResponseDTO()

        return response_dto.dump({"items": games, "count": count})


