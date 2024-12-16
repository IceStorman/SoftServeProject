import json

from flask import Response

from database.models import Sport, League
from api.routes.dto import SportsLeagueDTO, SportsLeagueOutputDTO, SportsOutputDTO
from exept.handle_exeptions import handle_exceptions

@handle_exceptions
def get_all_sports(session):
    sports = session.query(Sport).all()
    return [
        SportsOutputDTO(
            id=sport.sport_id,
            sport=sport.sport_name,
            logo=sport.sport_img,
        ).to_dict() for sport in sports
    ]


@handle_exceptions
def get_all_leagues_by_sport(session, dto: SportsLeagueDTO):
    offset = (dto.page - 1) * dto.per_page
    leagues = (
        session.query(League)
        .join(Sport, Sport.sport_id == League.sport_id)
        .filter(Sport.sport_name == dto.sport)
        .limit(dto.per_page)
        .offset(offset)
        .all()
    )
    return [
        {
            "_id": league.league_id,
            "name": league.name,
            "logo": league.logo,
            "sport_name": dto.sport
        }
        for league in leagues
    ]

