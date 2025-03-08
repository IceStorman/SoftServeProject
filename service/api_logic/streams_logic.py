import json
from database.models.streams import Stream
from database.models.streams_status import Streams_Status
from sqlalchemy.sql.expression import ClauseElement
from dto.api_output import StreamsOutput, StreamUrl
from exept.handle_exeptions import handle_exceptions
from logger.logger import Logger
from service.api_logic.scripts import get_sport_index_by_name
from sqlalchemy.orm import aliased
import datetime


class StreamService:

    def __init__(self, stream_dal):
        self._stream_dal = stream_dal
        self._logger = Logger("logger", "all.log").logger


    def get_streams_filtered(self, filters_dto): #not working for now without Roman's PR, Roman will fix in future
        pass
        # query = self._stream_dal.get_base_query(Stream)
        #
        # query = FilterManagerStrategy.apply_filters(Stream, query, filters_dto)
        # count = query.count()
        #
        # streams = self._stream_dal.execute_query(query)
        # streams_output = StreamsOutput(many=True)
        # stream = streams_output.dump(streams)
        #
        # return {
        #     "count": count,
        #     "stream": stream,
        # }


    def save_json_stream_to_streams_table(self, streams_data):
        streams_list = json.loads(streams_data) if isinstance(streams_data, str) else streams_data

        self._stream_dal.save_streams(streams_list)


    def save_json_stream_to_status_table(self, streams_status_data):
        streams_status_list = json.loads(streams_status_data) if isinstance(streams_status_data, str) else streams_status_data

        self._stream_dal.save_stream_statuses(streams_status_list)


    def all_streams(self): # Honestly, don't really see a sense of this method, as we have filters, but as long as we didn't merge Roman's PR we need it
        streams = self._stream_dal.get_all_streams()

        streams_output = StreamsOutput(many=True)
        stream = streams_output.dump(streams)

        return stream