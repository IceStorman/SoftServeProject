from api.routes.dto import GamesDTO, GameOutputDTO
from database.models import Games, Country, TeamIndex, League, Sport
from exept.handle_exeptions import handle_exceptions
from service.api_logic.scripts import apply_filters
from sqlalchemy.orm import aliased

@handle_exceptions
def get_games_today(
        session,
        filters_dto: GamesDTO
):
    home_team = aliased(TeamIndex)
    away_team = aliased(TeamIndex)

    query = (
        session.query(
            Games.game_id,
            Games.sport_id,
            Games.league_id,
            Games.country_id,
            Games.status,
            Games.date,
            Games.time,
            Games.score_away_team,
            Games.score_home_team,
            League.name.label("league_name"),
            League.logo.label("league_logo"),
            Country.name.label("country_name"),
            home_team.name.label("home_team_name"),
            home_team.logo.label("home_team_logo"),
            away_team.name.label("away_team_name"),
            away_team.logo.label("away_team_logo"),
        )
        .join(League, Games.league_id == League.league_id)
        .join(Country, Games.country_id == Country.country_id)
        .join(Sport, Games.sport_id == Sport.sport_id)
        .join(home_team, Games.team_home_id == home_team.team_index_id)
        .join(away_team, Games.team_away_id == away_team.team_index_id)
    )

    model_aliases = {
        "games": Games,
    }

    query = apply_filters(query, filters_dto.to_dict(), model_aliases)

    offset, limit = filters_dto.get_pagination()

    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)

    games = query.all()

    return [
        GameOutputDTO(
            game_id=game.game_id,
            status=game.status,
            date=game.date,
            time=game.time,
            league_name=game.league_name,
            league_logo=game.league_logo,
            country_name=game.country_name,
            home_team_name=game.home_team_name,
            home_team_logo=game.home_team_logo,
            away_team_name=game.away_team_name,
            away_team_logo=game.away_team_logo,
            home_score=game.score_home_team,
            away_score=game.score_away_team,
        ).to_dict()
        for game in games
    ]


