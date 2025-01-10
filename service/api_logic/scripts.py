from marshmallow import Schema

from database.models import Sport, League
from exept.exeptions import SportNotFoundError
from sqlalchemy.orm import Query
from sqlalchemy import and_
from logger.logger import get_logger, log_function_call

api_logic_logger = get_logger("api_logic_logger", "api_logic.log")

@log_function_call(api_logic_logger)
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





@log_function_call(api_logic_logger)
def apply_filters(base_query: Query, filters: dict, model_aliases: dict):
    filter_conditions = []

    for key, value in filters.items():
        if "__" in key:
            if value is None:
                continue
            table_name, column_name = key.split("__")
            model = model_aliases.get(table_name, None)
            if model is None:
                raise ValueError(f"Model alias '{table_name}' not in model_aliases.")

            column = getattr(model, column_name, None)

            if column is not None:
                filter_conditions.append(column == value)
            else:
                raise ValueError(f"Column '{column_name}' not in model '{table_name}'.")
        else:
            continue
    if filter_conditions:
        base_query = base_query.filter(and_(*filter_conditions))
        api_logic_logger.info(f"These filter conditions were used: {filter_conditions}")
    else:
        api_logic_logger.warning(f"Filter conditions: {filter_conditions} weren't applied")

    return base_query



