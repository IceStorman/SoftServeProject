import json
from database.models.streams import Stream
from database.models.streams_status import Streams_Status
from database.models.statuses import Statuses
from sqlalchemy.sql.expression import ClauseElement
from exept.handle_exeptions import handle_exceptions
from service.api_logic.scripts import get_sport_index_by_name
from dto.pagination import Pagination
from sqlalchemy.orm import aliased
import datetime

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
def get_streams_today(pagination, session):

    StreamsStatus = aliased(Streams_Status)


    query = (
        session.query(
            Stream.stream_id,
            Stream.stream_url,
            Stream.start_time,
            Stream.sport_id,
            StreamsStatus.status_id
        )
        .join(StreamsStatus, Stream.stream_id == StreamsStatus.stream_id)
    )

    today_start = datetime.combine(datetime.date.today(), datetime.min.time())
    today_end = datetime.combine(datetime.date.today(), datetime.max.time())
    query = query.filter(
        Stream.start_time.between(today_start.timestamp(), today_end.timestamp())
    )


    if pagination:
        query = query.offset(pagination.offset).limit(pagination.limit)

    return query.all()


@handle_exceptions
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
def get_streams_by_count(session, count:int):
    streams = fetch_streams(session, order_by=Stream.start_time.desc(), limit=count)
    return json_streams(streams)

@handle_exceptions
def get_latest_sport_streams(session, count:int, sport_name:str):
    sport = get_sport_index_by_name(session, sport_name)
    filters = [Stream.sport_id == sport.sport_id]
    streams = fetch_streams(session, order_by=Stream.start_time.desc(), limit=count, filters=filters)
    return json_streams(streams)

@handle_exceptions
def get_streams_of_sport(session, sport_name:str):
    sport = get_sport_index_by_name(session, sport_name)
    filters = [Stream.sport_id == sport.sport_id]
    streams = fetch_streams(session, order_by=Stream.start_time.desc(), filters=filters)
    return json_streams(streams)



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

