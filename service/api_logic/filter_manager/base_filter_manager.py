from sqlalchemy.orm import Query

class BaseFilterManager:
    FILTERS ={}

    @classmethod
    def apply_filters(cls, query: Query, dto_instance) -> Query:
        if dto_instance is None:
            return query

        dto_fields = getattr(dto_instance, "_fields", {})

        for field_name in dto_fields:
            field_value = getattr(dto_instance, field_name, None)

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

        return query