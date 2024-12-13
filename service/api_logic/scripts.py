from database.models import Sport, Games, League, Country, TeamIndex
from exept.exeptions import SportNotFoundError
from api.routes.dto import UniversalResponseDTO

def get_sport_by_name(session, sport_name):
    sport = session.query(Sport).filter(Sport.sport_name == sport_name).first()
    if not sport:
        raise SportNotFoundError(sport_name)
    return sport
