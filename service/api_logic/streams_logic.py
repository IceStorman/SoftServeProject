import json
from database.models.streams import Stream
from database.models.streams_status import Streams_Status
from sqlalchemy.sql.expression import ClauseElement
from exept.handle_exeptions import handle_exceptions
from logger.logger import Logger
from service.api_logic.scripts import get_sport_index_by_name
from sqlalchemy.orm import aliased
import datetime


class StreamService:

    def __init__(self, streams_dal):
        self._stream_dal = streams_dal
        self._logger = Logger("logger", "all.log").logger


    # def get_streams_today(self, pagination, session):
    #
    #     StreamsStatus = aliased(Streams_Status)
    #
    #
    #     # query = (
    #     #     session.query(
    #     #         Stream.stream_id,
    #     #         Stream.stream_url,
    #     #         Stream.start_time,
    #     #         Stream.sport_id,
    #     #         StreamsStatus.status_id
    #     #     )
    #     #     .join(StreamsStatus, Stream.stream_id == StreamsStatus.stream_id)
    #     # ) Roman filters applied later
    #
    #     today_start = datetime.combine(datetime.date.today(), datetime.min.time())
    #     today_end = datetime.combine(datetime.date.today(), datetime.max.time())
    #     query = query.filter(
    #         Stream.start_time.between(today_start.timestamp(), today_end.timestamp())
    #     )
    #
    #
    #     if pagination:
    #         query = query.offset(pagination.offset).limit(pagination.limit)
    #
    #     return query.all()


    def save_json_stream_to_streams_table(self, streams_data):
        streams_list = json.loads(streams_data) if isinstance(streams_data, str) else streams_data

        self._stream_dal.save_streams(streams_list)


    def save_json_stream_to_status_table(self, streams_status_data):
        streams_status_list = json.loads(streams_status_data) if isinstance(streams_status_data, str) else streams_status_data

        self._stream_dal.save_stream_statuses(streams_status_list)


    def all_streams(self):
        streams = self._stream_dal.get_all_streams()
        streams_data = []
        for stream in streams:
            streams_data.append({
                "stream_id":stream.stream_id,
                "stream_url":stream.stream_url,
                "start_time":stream.start_time,
                "sport_id":stream.sport_id
            })
        return json.dumps(streams_data, ensure_ascii=False)