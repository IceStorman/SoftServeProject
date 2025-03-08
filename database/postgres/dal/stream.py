from rich.spinner import Spinner
from sqlalchemy import func

from database.models import Stream, Streams_Status, StreamUrl
from database.postgres.dto import StreamDTO, StreamStatusDTO
from typing import List


class StreamDAL:
    def __init__(self, session = None):
        self.db_session = session

    def create_stream(self, stream_dto: StreamDTO) -> Stream:
        new_stream = Stream(
            stream_url = stream_dto.stream_url,
            start_time = stream_dto.start_time,
            sport_id = stream_dto.sport_id
        )

        self.db_session.add(new_stream)
        self.db_session.commit()

        return new_stream

    def create_stream_status(self, status_dto: StreamStatusDTO) -> Streams_Status:
        new_stream_status = Streams_Status(
            stream_id = status_dto.stream_id,
            status_id = status_dto.status_id,
        )

        self.db_session.add(new_stream_status)
        self.db_session.commit()

        return new_stream_status


    def save_streams(self, streams_dto_list: List[StreamDTO]):
        for stream in streams_dto_list:
            self.create_stream(stream)

    def save_stream_statuses(self, status_dto_list: List[StreamStatusDTO]):
        for status in status_dto_list:
            self.create_stream_status(status)

    def get_all_streams(self):
        result = (self.db_session.query(
            Stream.stream_id,
            Stream.title,
            Stream.start_time,
            Stream.sport_id,
            func.array_agg(StreamUrl.stream_url).label('stream_url')
        ).join(
            StreamUrl,
            Stream.stream_id == StreamUrl.stream_id
        ).group_by(
            Stream.stream_id
        ).all())

        return result
