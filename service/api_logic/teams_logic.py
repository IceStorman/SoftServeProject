from dto.api_input import TeamsLeagueDTO
from exept.handle_exeptions import handle_exceptions
from database.models import TeamIndex, Sport, League, Country
from service.api_logic.scripts import apply_filters
from dto.api_output import TeamsLeagueOutputDTO


# NOT WORK NOW ----------------------------------

@handle_exceptions
def get_teams(
        session,
        filters_dto: TeamsLeagueDTO
):
    query = (
        session.query(
            TeamIndex.league,
            TeamIndex.team_index_id,
            TeamIndex.sport_id,
            TeamIndex.country,
            TeamIndex.league,
            TeamIndex.api_id,
            TeamIndex.logo,
            TeamIndex.name,
            TeamIndex.news_id
        )
         .join(League, TeamIndex.league == League.league_id)
         .join(Country, TeamIndex.country == Country.country_id)
         .join(Sport, TeamIndex.sport_id == Sport.sport_id)
    )

    model_aliases = {
        "teams": TeamIndex,
        "countries": Country,
        "leagues": League,
    }

    query = apply_filters(query, filters_dto.to_dict(), model_aliases)

    offset, limit = filters_dto.get_pagination()

    if offset is not None and limit is not None:
        query = query.offset(offset).limit(limit)

    teams = query.all()
    return [
        TeamsLeagueOutputDTO(
            league_name=team.league,
            country_name=team.country,
            team_name=team.name,
            logo=team.logo,
            id=team.api_id,
        ).to_dict() for team in teams
    ]





