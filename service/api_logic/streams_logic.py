import json
from database.models import Stream
from sqlalchemy.sql.expression import ClauseElement
from exept.handle_exeptions import handle_exceptions
from service.api_logic.scripts import get_sport_index_by_name

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
def get_streams_by_count(session, count:int):
    streams = fetch_streams(session, order_by=Stream.save_at.desc(), limit=count)
    return json_streams(streams)

@handle_exceptions
def get_latest_sport_streams(session, count:int, sport_name:str):
    sport = get_sport_index_by_name(session, sport_name)
    filters = [Stream.sport_id == sport.sport_id]
    streams = fetch_streams(session, order_by=Stream.save_at.desc(), limit=count, filters=filters)
    return json_streams(streams)

@handle_exceptions
def get_streams_of_sport(session, sport_name:str):
    sport = get_sport_index_by_name(session, sport_name)
    filters = [Stream.sport_id == sport.sport_id]
    streams = fetch_streams(session, order_by=Stream.save_at.desc(), filters=filters)
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

