from database.models import Sport, League
from exept.colors_text import print_error_message
from exept.handle_exeptions import handle_exceptions
from api.routes.dto import SportsLeagueDTO, SportsLeagueOutputDTO, SportsOutputDTO

@handle_exceptions
def get_all_sports(session):
    sports = session.query(Sport).all()
    if not sports:
        print_error_message("No sports found in the database")
        return [], 204

    return [
        SportsOutputDTO(
            id=sport.sport_id,
            sport=sport.sport_name,
            logo=sport.sport_img,
        ) for sport in sports
    ], 200


@handle_exceptions
def get_all_leagues_by_sport(session, dto: SportsLeagueDTO):
    if dto.sport is None:
        return {"error": "Not param sport_name"}
    offset = (dto.page - 1) * dto.per_page
    leagues = (
        session.query(League)
        .join(Sport, Sport.sport_id == League.sport_id)
        .filter(Sport.sport_name == dto.sport)
        .limit(dto.per_page)
        .offset(offset)
        .all()
    )
    if not leagues:
        print_error_message("No leagues found for the sport")
        return [], 204

    return [
        SportsLeagueOutputDTO(
            id=league.league_id,
            sport=league.name,
            logo=league.logo,
            name=dto.sport,
        ) for league in leagues
    ], 200