from database.models import Sport
from exept.exeptions import SportNotFoundError

def get_sport_by_name(session, sport_name):
    sport = session.query(Sport).filter(Sport.sport_name == sport_name).first()
    if not sport:
        raise SportNotFoundError(sport_name)
    return sport