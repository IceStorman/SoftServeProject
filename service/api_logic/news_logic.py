import json
from flask import Response
from database.models import News
from database.azure_blob_storage.save_get_blob import blob_get_news
from sqlalchemy.sql.expression import ClauseElement
from exept.handle_exeptions import handle_exceptions
from service.api_logic.scripts import get_sport_by_name
from database.session import SessionLocal
from logger.logger import Logger

logger = Logger("api_logic_logger", "api_logic_logger.log")

session = SessionLocal()

@logger.log_function_call()
def fetch_news(session, order_by: ClauseElement = None, limit: int = None, filters=None):
    query = session.query(News)
    if filters:
        query = query.filter(*filters)
    if order_by is not None:
        query = query.order_by(order_by)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


@handle_exceptions
@logger.log_function_call()
def get_news_by_count(count: int):
    news = fetch_news(session, order_by=News.save_at.desc(), limit=count)
    return json_news(news)


@handle_exceptions
@logger.log_function_call()
def get_latest_sport_news(count: int, sport_name: str):
    sport = get_sport_by_name(session, sport_name)

    filters = [News.sport_id == sport.sport_id]
    news = fetch_news(session, order_by=News.save_at.desc(), limit=count, filters=filters)
    return json_news(news)


@handle_exceptions
@logger.log_function_call()
def get_popular_news(count: int):
    news = fetch_news(session, order_by=News.interest_rate.desc(), limit=count)
    return json_news(news)

@handle_exceptions
@logger.log_function_call()
def get_news_by_id(blob_id: str):
    news = fetch_news(session, filters=[News.blob_id == blob_id], limit=1)
    if news:
        logger.warning(f"News ware`t empty: {news}")
        return json_news(news)



@logger.log_function_call()
def json_news(news_records):
    all_results = []
    for news_record in news_records:
        data = blob_get_news(news_record.blob_id)
        all_results.append({
            "blob_id": news_record.blob_id,
            "data": data
        })
    return Response(
        json.dumps(all_results, ensure_ascii=False),
        content_type='application/json; charset=utf-8',
    )
