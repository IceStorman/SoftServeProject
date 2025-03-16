import json
from dto.api_output import StreamsOutput
from logger.logger import Logger
from database.postgres.dto import StreamStatusDTO, StreamUrlDTO


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


    def save_streams_to_streams_table(self, streams_data):
        for stream in streams_data:
            if stream.stream_urls:
                new_stream = self._stream_dal.create_stream(stream)
                for url in stream.stream_urls:
                    new_url = StreamUrlDTO(
                        stream_url=url,
                        stream_id=new_stream.stream_id
                    )
                    self._stream_dal.create_stream_url(new_url)

        

    def save_json_stream_to_status_table(self, streams_status_data):
        streams_status_list = json.loads(streams_status_data) if isinstance(streams_status_data, str) else streams_status_data

        self._stream_dal.save_stream_statuses(streams_status_list)


    def all_streams(self): # Honestly, don't really see a sense of this method, as we have filters, but as long as we didn't merge Roman's PR we need it
        streams = self._stream_dal.get_all_streams()

        streams_output = StreamsOutput(many=True)
        stream = streams_output.dump(streams)

        return stream