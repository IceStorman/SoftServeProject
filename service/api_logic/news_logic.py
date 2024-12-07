import json
from flask import Response
from database.models import News
from database.azure_blob_storage.save_get_blob import blob_get_news
from sqlalchemy.sql.expression import ClauseElement
from exept.exeptions import SportNotFoundError, BlobFetchError
from service.api_logic.scripts import get_sport_by_name
from api.routes.scripts import get_error_response

def fetch_news(session, order_by: ClauseElement = None, limit: int = None, filters=None):
    query = session.query(News)
    if filters:
        query = query.filter(*filters)
    if order_by is not None:
        query = query.order_by(order_by)
    if limit is not None:
        query = query.limit(limit)
    return query.all()


def get_news_by_count(count: int, session):
    try:
        news = fetch_news(session, order_by=News.save_at.desc(), limit=count)
        return json_news(news)
    except Exception:
        raise Exception


def get_latest_sport_news(count: int, sport_name: str, session):
    try:
        sport = get_sport_by_name(session, sport_name)
    except SportNotFoundError as e:
        return get_error_response({"error": e.message },404)
    filters = [News.sport_id == sport.sport_id]
    news = fetch_news(session, order_by=News.save_at.desc(), limit=count, filters=filters)
    return json_news(news)


def get_popular_news(count: int, session):
    try:
        news = fetch_news(session, order_by=News.interest_rate.desc(), limit=count)
        return json_news(news)
    except Exception:
        raise Exception


def json_news(news_records):
    all_results = []
    for news_record in news_records:
        try:
            data = blob_get_news(news_record.blob_id)
            all_results.append({
                "blob_id": news_record.blob_id,
                "data": data
            })
        except BlobFetchError as e:
            return get_error_response({"error": e.message },502)
    return Response(
        json.dumps(all_results, ensure_ascii=False),
        content_type='application/json; charset=utf-8',
        status=200
    )
