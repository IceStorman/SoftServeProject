from sqlalchemy import cast
from database.models import Stream
from service.api_logic.filter_manager.base_filter_manager import BaseFilterManager
from sqlalchemy.orm import Query
from sqlalchemy.sql.sqltypes import Time


class StreamsFilterManager(BaseFilterManager):

    @staticmethod
    def apply_sport_id_filter(query: Query, value: int) -> Query:
        return query.filter(Stream.sport_id == value)

    @staticmethod
    def apply_stream_id_filter(query: Query, value: int) -> Query:
        return query.filter(Stream.stream_id == value)

    @staticmethod
    def apply_title_contains(query: Query, value: str) -> Query:
        return query.filter(Stream.title.ilike(f"%{value}%"))

    @staticmethod
    def apply_time_from_filter(query: Query, value: str) -> Query:
        return query.filter(cast(Stream.start_time, Time) >= value)


    FILTERS = {
        "sport_id": apply_sport_id_filter,
        "title_contains": apply_title_contains,
        "time_from": apply_time_from_filter,
        "stream_id": apply_stream_id_filter
    }