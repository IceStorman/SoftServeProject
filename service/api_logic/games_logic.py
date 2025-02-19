from dto.api_output import GameOutput
from dto.api_input import GamesDTO
from database.models import Games, Country, TeamIndex, League, Sport
from dto.pagination import Pagination
from exept.handle_exeptions import handle_exceptions
from sqlalchemy.orm import aliased
from database.session import SessionLocal
from logger.logger import Logger
from service.api_logic.filter_manager.filter_manager_factory import FilterManagerFactory

logger = Logger("logger", "all.log")

class GamesService:
    def __init__(self, games_dal):
        self._games_dal = games_dal
        self._logger = Logger("logger", "all.log").logger

    def get_games_today(self, filters_dto: GamesDTO(), pagination: Pagination):
        # home_team = aliased(TeamIndex)
        # away_team = aliased(TeamIndex)

        # query = (
        #     session.query(
        #         Games,
        #         League.name.label("league_name"),
        #         League.logo.label("league_logo"),
        #         Country.name.label("country_name"),
        #         home_team.name.label("home_team_name"),
        #         home_team.logo.label("home_team_logo"),
        #         away_team.name.label("away_team_name"),
        #         away_team.logo.label("away_team_logo"),
        #         Games.score_home_team,
        #         Games.score_away_team,
        #         Games.status,
        #         Games.time,
        #         Games.date,
        #         Games.api_id
        #     )
        #     .join(League, Games.league_id == League.league_id)
        #     .join(Country, Games.country_id == Country.country_id)
        #     .join(Sport, Games.sport_id == Sport.sport_id)
        #     .join(home_team, Games.team_home_id == home_team.team_index_id)
        #     .join(away_team, Games.team_away_id == away_team.team_index_id)
        # )

        query = self._games_dal.get_query()

        model_aliases = {
            "games": Games,
            "countries": Country,
            "leagues": League,
        }

        filtered_query = FilterManagerFactory.apply_filters(Games, query, filters_dto)

        offset, limit = pagination.get_pagination()
        if offset is not None and limit is not None:
            filtered_query = filtered_query.offset(offset).limit(limit)

        games = self._games_dal.execute_query(filtered_query)

        schema = GameOutput(many=True)
        return schema.dump(games)


