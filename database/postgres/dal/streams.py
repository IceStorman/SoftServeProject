from sqlalchemy.orm import Session
from database.models import Stream
from database.postgres.dto import StreamDTO
from typing import Optional
from dto.api_output import SportsOutput


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
        self.db_session.refresh(new_stream)

        return new_stream

