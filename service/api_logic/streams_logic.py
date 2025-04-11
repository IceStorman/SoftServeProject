import json
from sqlalchemy import func
from dto.api_output import StreamsOutput, ListResponseDTO
from logger.logger import Logger
from database.postgres.dto import StreamUrlDTO
from database.models import Stream, StreamUrl
from service.api_logic.filter_manager.filter_manager_strategy import FilterManagerStrategy


class StreamService:
    def __init__(self, stream_dal):
        self._stream_dal = stream_dal
        self._logger = Logger("logger", "all.log").logger


    def get_streams_filtered(self, filters_dto):
        query = (self._stream_dal.get_base_query(Stream).with_entities(
            Stream.stream_id,
            Stream.title,
            Stream.start_time,
            Stream.sport_id,
            func.array_agg(StreamUrl.stream_url).label('stream_url')
        )
         .join(StreamUrl, Stream.stream_id == StreamUrl.stream_id)
         .group_by(Stream.stream_id)
        )

        filtered_query, count = FilterManagerStrategy.apply_filters(Stream, query, filters_dto)

        streams = self._stream_dal.query_output(filtered_query)
        stream_output = StreamsOutput(many=True).dump(streams)
        response_dto = ListResponseDTO(items = stream_output, count = count)

        return response_dto.to_dict()


    def save_streams_with_urls(self, streams_data):
        for stream in streams_data:
            if stream.stream_urls:
                self._stream_dal.save_stream_with_urls(stream)