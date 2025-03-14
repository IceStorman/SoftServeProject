from marshmallow import Schema

from database.models import Sport, League
from exept.exeptions import SportNotFoundError
from sqlalchemy.orm import Query
from sqlalchemy import and_
from logger.logger import Logger

logger = Logger("logger", "all.log")

@logger.log_function_call()
def get_sport_by_name(session, sport_name):
    sport = session.query(Sport).filter(Sport.sport_name == sport_name).first()
    if not sport:
        raise SportNotFoundError(sport_name)
    return sport

def get_sport_index_by_name(session, sport_name):
    sport = session.query(Sport).filter(Sport.sport_name == sport_name).first()
    if not sport:
        raise SportNotFoundError(sport_name)
    return sport.sport_id




