from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Stream, Streams_Status, StreamUrl
from database.postgres.dal.base import BaseDAL
from database.postgres.dto import StreamDTO, StreamStatusDTO, StreamUrlDTO
from typing import List


class StreamDAL(BaseDAL):
    def __init__(self, session: Session):
        self.session = session


    def create_stream(self, stream_dto: StreamDTO) -> Stream:
        new_stream = Stream(
            title = stream_dto.title,
            start_time = stream_dto.start_time,
            sport_id = stream_dto.sport_id
        )

        self.session.add(new_stream)
        self.session.flush()

        return new_stream


    def save_stream_with_urls(self, stream_dto):
        try:
            new_stream = self.create_stream(stream_dto)

            for url in stream_dto.stream_urls:
                new_url = StreamUrlDTO(
                    stream_url=url,
                    stream_id=new_stream.stream_id
                )
                self.create_stream_url(new_url)

            self.session.commit()
            return new_stream

        except SQLAlchemyError:
            self.session.rollback()


    def create_stream_url(self, url_dto: StreamUrlDTO):
        new_url = StreamUrl(
            stream_id=url_dto.stream_id,
            stream_url=url_dto.stream_url,
        )

        self.session.add(new_url)


    def save_stream_urls(self, url_dto_list: List[StreamUrlDTO]):
        for url in url_dto_list:
            self.create_stream_url(url)


    def create_stream_status(self, status_dto: StreamStatusDTO) -> Streams_Status:
        new_stream_status = Streams_Status(
            stream_id = status_dto.stream_id,
        )

        self.session.add(new_stream_status)
        self.session.commit()

        return new_stream_status


    def save_stream_statuses(self, status_dto_list: List[StreamStatusDTO]):
        for status in status_dto_list:
            self.create_stream_status(status)