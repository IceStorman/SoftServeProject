from sqlalchemy.orm import Query
from typing import Optional
from dto.pagination import Pagination
from sqlalchemy import desc, asc

from sqlalchemy.orm import Query
from sqlalchemy import asc, desc

class BaseFilterManager:
    FILTERS = {}

    @classmethod
    def apply_filters(cls, query: Query, dto) -> tuple[Query, int]:
        if dto is None:
            return query, query.count()

        filters_list = getattr(dto, "filters", [])

        for filter_obj in filters_list:
            filter_name = getattr(filter_obj, "name", None)
            filter_value = getattr(filter_obj, "value", None)

            if filter_name in cls.FILTERS and filter_value is not None:
                query = cls.FILTERS[filter_name](query, filter_value)

        order_field = getattr(dto, "field", None)
        order_type = getattr(dto, "order", None)

        if order_field and order_type:
            order_func = asc if order_type.lower() == "asc" else desc
            first_model = query.column_descriptions[0]["entity"]
            if hasattr(first_model, order_field):
                query = query.order_by(order_func(getattr(first_model, order_field)))

        count = query.count()

        pagination_dto = getattr(dto, "pagination", None)
        if pagination_dto:
            offset = (pagination_dto.page - 1) * pagination_dto.per_page
            query = query.offset(offset).limit(pagination_dto.per_page)

        return query, count