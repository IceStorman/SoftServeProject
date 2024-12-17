from database.models import Sport, Games, League, Country, TeamIndex
from exept.exeptions import SportNotFoundError
from api.routes.dto import UniversalResponseDTO

def get_sport_by_name(session, sport_name):
    sport = session.query(Sport).filter(Sport.sport_name == sport_name).first()
    if not sport:
        raise SportNotFoundError(sport_name)
    return sport


#-------------------------------------

# def apply_filters(query, dto: BaseModel):
#     filters = []
#     for field, value in dto.dict(exclude_unset=True).items():
#         if value is not None:
#             column = getattr(dto.__class__, field, None)
#             if column:
#                 filters.append(getattr(column, "name") == value)
#     if filters:
#         query = query.filter(*filters)
#
#     return query



from sqlalchemy.orm import Query
from typing import Type
from pydantic import BaseModel
from database.models.base import Base

def apply_filters(query, model: Type[Base], dto: BaseModel):
    filters = []
    for field, value in dto.dict(exclude_unset=True).items():
        if value is not None:
            column = getattr(model, field, None)
            if column:
                filters.append(column == value)
            else:
                raise ValueError(f"Field '{field}' not found in model '{model.__name__}'")
    if filters:
        query = query.filter(*filters)

    return query