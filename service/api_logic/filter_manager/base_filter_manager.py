from sqlalchemy.orm import Query
from typing import Optional
from dto.pagination import Pagination

class BaseFilterManager:
    FILTERS ={}

    @classmethod
    def apply_filters(cls, query: Query, dto) -> Query:
        if dto is None:
            return query

        dto_fields = getattr(dto, "_fields", {})

        for field_name in dto_fields:
            field_value = getattr(dto, field_name, None)

            if field_value is None:
                continue
            if hasattr(field_value, "_fields"):
                query = cls.apply_filters(query, field_value)

            elif isinstance(field_value, list):
                for model_dto in field_value:
                    if hasattr(model_dto, "_fields"):
                        query = cls.apply_filters(query, model_dto)

            elif field_name in cls.FILTERS:
                filter_method = cls.FILTERS[field_name]
                query = filter_method(query, field_value)

        pagination_dto = getattr(dto, "pagination", None)
        if pagination_dto:
            pagination = Pagination(page=pagination_dto.page, per_page=pagination_dto.per_page)
            offset, limit = pagination.get_pagination()
            query = query.offset(offset).limit(limit)

        return query