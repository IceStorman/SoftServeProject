from sqlalchemy.orm import Query

class BaseFilterManager:
    FILTERS ={}

    @classmethod
    def apply_filters(cls, query: Query, filters: dict, session) -> Query:
        for filter_name, filter_value in filters.items():
            if filter_name in cls.FILTERS and filter_value:
                filter_method = getattr(cls, cls.FILTERS[filter_name])
                if filter_name == "sport":
                    query = filter_method(query, filter_value, session)
                else:
                    query = filter_method(query, filter_value)
        return query