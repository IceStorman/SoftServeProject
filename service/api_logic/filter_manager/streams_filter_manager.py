from sqlalchemy import cast
from database.models import Stream
from service.api_logic.filter_manager.base_filter_manager import BaseFilterManager
from sqlalchemy.orm import Query
from sqlalchemy.sql.sqltypes import Time, Date


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
    def apply_date_from(query: Query, value: str) -> Query:
        return query.filter(cast(Stream.start_time, Date) >= value)


    FILTERS = {
        "sport_id": apply_sport_id_filter,
        "name": apply_title_contains,
        "date_from": apply_date_from,
        "stream_id": apply_stream_id_filter
    }