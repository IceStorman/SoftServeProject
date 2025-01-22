import json
from database.models.streams import Stream
from database.models.streams_status import Streams_Status
from sqlalchemy.sql.expression import ClauseElement
from exept.handle_exeptions import handle_exceptions
from service.api_logic.scripts import get_sport_index_by_name
from logger.logger import Logger

api_logic_logger = Logger("api_logic_logger", "api_logic_logger.log")

@api_logic_logger.log_function_call()
def fetch_streams(session, order_by: ClauseElement = None, limit: int = None, filters=None):
    query = session.query(Stream)
    if filters:
        query = query.filter(*filters)
    if order_by is not None:
        query = query.order_by(order_by)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


@handle_exceptions
@api_logic_logger.log_function_call()
def save_json_stream_to_streams_table(session, streams_data):
    streams_list = json.loads(streams_data) if isinstance(streams_data, str) else streams_data

    for stream_data in streams_list:
        stream = Stream(
                stream_url=stream_data["stream_url"],
                sport_id=stream_data["sport_id"],
        )

        session.merge(stream)  
    session.commit()

@handle_exceptions
@api_logic_logger.log_function_call()
def save_json_stream_to_status_table(session,streams_data):
    streams_list = json.loads(streams_data) if isinstance(streams_data, str) else streams_data

    for stream_data in streams_list:
        stream = Streams_Status(
            start_time=stream_data["time"],
            status=stream_data["status"]

        )

        session.merge(stream)
    
    session.commit()




@handle_exceptions
@api_logic_logger.log_function_call()
def get_streams_by_count(session, count:int):
    streams = fetch_streams(session, order_by=Stream.start_time.desc(), limit=count)
    return json_streams(streams)

@handle_exceptions
@api_logic_logger.log_function_call()
def get_latest_sport_streams(session, count:int, sport_name:str):
    sport = get_sport_index_by_name(session, sport_name)
    filters = [Stream.sport_id == sport.sport_id]
    streams = fetch_streams(session, order_by=Stream.start_time.desc(), limit=count, filters=filters)
    return json_streams(streams)

@handle_exceptions
@api_logic_logger.log_function_call()
def get_streams_of_sport(session, sport_name:str):
    sport = get_sport_index_by_name(session, sport_name)
    filters = [Stream.sport_id == sport.sport_id]
    streams = fetch_streams(session, order_by=Stream.start_time.desc(), filters=filters)
    return json_streams(streams)



@api_logic_logger.log_function_call()
def json_streams(session):
    streams = session.query(Stream).all()
    streams_data = []
    for stream in streams:
        streams_data.append({
            "stream_id":stream.stream_id,
            "stream_url":stream.stream_url,
            "start_time":stream.start_time,
            "status":stream.status,
            "sport_id":stream.sport_id
        })
    return json.dumps(streams_data, ensure_ascii=False)

