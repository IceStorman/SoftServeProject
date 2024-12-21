from database.models import Sport, Games, League, Country, TeamIndex
from exept.exeptions import SportNotFoundError

def get_sport_by_name(session, sport_name):
    sport = session.query(Sport).filter(Sport.sport_name == sport_name).first()
    if not sport:
        raise SportNotFoundError(sport_name)
    return sport




from sqlalchemy.orm import Query
from typing import Type
from pydantic import BaseModel
from database.models.base import Base

# def apply_filters(query, model: Type[Base], dto: BaseModel):
#     filters = []
#     for field, value in dto.dict(exclude_unset=True).items():
#         if value is not None:
#             column = getattr(model, field, None)
#             if column:
#                 filters.append(column == value)
#             else:
#                 raise ValueError(f"Field '{field}' not found in model '{model.__name__}'")
#     if filters:
#         query = query.filter(*filters)
#
#     return query

from sqlalchemy import and_

# def apply_filters(base_query: Query, filters: dict, model_aliases: dict):
#     filter_conditions = []
#
#     for key, value in filters.items():
#         if "." in key:
#             table_name, column_name = key.split(".")
#             model = model_aliases.get(table_name, None)
#             if model is None:
#                 raise ValueError(f"Model alias '{table_name}' не знайдено в model_aliases.")
#
#             column = getattr(model, column_name, None)
#             if column is not None:
#                 filter_conditions.append(column == value)
#             else:
#                 raise ValueError(f"Column '{column_name}' не знайдено в моделі '{table_name}'.")
#         else:
#             raise ValueError(f"Формат фільтра '{key}' некоректний. Використовуйте 'table.column'.")
#
#     if filter_conditions:
#         base_query = base_query.filter(and_(*filter_conditions))
#
#     return base_query

def apply_filters(base_query: Query, filters: dict, model_aliases: dict):
    """
    Додає фільтри до SQLAlchemy-запиту з підтримкою `JOIN`.

    :param base_query: SQLAlchemy Query, що вже існує.
    :param filters: Словник із фільтрами, наприклад {"user.name": "John", "order.status": "completed"}.
    :param model_aliases: Словник відповідності моделей (або псевдонімів), наприклад {"user": User, "order": Order}.
    :return: SQLAlchemy Query із застосованими фільтрами.
    """
    filter_conditions = []

    for key, value in filters.items():
        if "." in key:
            table_name, column_name = key.split(".")
            model = model_aliases.get(table_name, None)
            if model is None:
                raise ValueError(f"Model alias '{table_name}' не знайдено в model_aliases.")

            column = getattr(model, column_name, None)
            if column is not None:
                filter_conditions.append(column == value)
            else:
                raise ValueError(f"Column '{column_name}' не знайдено в моделі '{table_name}'.")
        else:
            raise ValueError(f"Формат фільтра '{key}' некоректний. Використовуйте 'table.column'.")

    if filter_conditions:
        base_query = base_query.filter(and_(*filter_conditions))

    return base_query


