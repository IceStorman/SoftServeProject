from database.models import Sport, League
from exept.exeptions import SportNotFoundError
from sqlalchemy.orm import Query
from sqlalchemy import and_
from datetime import datetime

def get_sport_by_name(session, sport_name):
    sport = session.query(Sport).filter(Sport.sport_name == sport_name).first()
    if not sport:
        raise SportNotFoundError(sport_name)
    return sport


def get_leagues_count_by_sport(session, sport_id):
    count = session.query(League).join(Sport, League.sport_id == Sport.sport_id).filter(League.sport_id == sport_id).count()
    return count


def apply_filters(base_query: Query, filters: dict, model_aliases: dict):
    filter_conditions = []

    for key, value in filters.items():
        if "." in key:
            table_name, column_name = key.split(".")
            model = model_aliases.get(table_name, None)
            if model is None:
                raise ValueError(f"Model alias '{table_name}' не знайдено в model_aliases.")

            column = getattr(model, column_name, None)
            if column is not None:
                if column_name == "date":
                    try:
                        if isinstance(value, str):
                            value = datetime.fromisoformat(value)
                            value = value.strftime("%y-%m-%d")  # Форматування дати в формат yy-mm-dd
                        print(value)
                        print(column)

                        filter_conditions.append(column == value)
                    except ValueError:
                        raise ValueError(f"bad data format")
                else:
                    filter_conditions.append(column == value)
            else:
                raise ValueError(f"Column '{column_name}' not in model '{table_name}'.")
        else:
            raise ValueError(f"Filtr '{key}' not correct. Use 'table.column'.")

    if filter_conditions:
        base_query = base_query.filter(and_(*filter_conditions))
        print(base_query)

    return base_query


