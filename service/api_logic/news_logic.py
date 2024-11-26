import json
from database.models import News, Sport
from database.azure_blob_storage.save_get_blob import blob_get_news
from exept.colors_text import print_error_message
from sqlalchemy.sql.expression import ClauseElement


def fetch_news(session, order_by: ClauseElement = None, limit: int = None, filters=None):
    query = session.query(News)

    if filters:
        query = query.filter(*filters)

    if order_by is not None:
        query = query.order_by(order_by)

    if limit is not None:
        query = query.limit(limit)

    return query.all()


# Використання:
def get_news_by_count(count: int, session):
    news = fetch_news(session, order_by=News.save_at.desc(), limit=count)
    return json_news(news)


def get_latest_sport_news(count: int, sport_name: str, session):
    sport = session.query(Sport).filter(Sport.sport_name == sport_name).first()
    if not sport:
        return {"error": f"Sport '{sport_name}' not found"}

    filters = [News.sport_id == sport.sport_id]
    news = fetch_news(session, order_by=News.save_at.desc(), limit=count, filters=filters)
    return json_news(news)


def get_popular_news(count: int, session):
    news = fetch_news(session, order_by=News.interest_rate.desc(), limit=count)
    return json_news(news)


def json_news(news_records):
    all_results = []
    for news_record in news_records:
        try:
            data = blob_get_news(news_record.blob_id)
            all_results.append({
                "blob_id": news_record.blob_id,
                "data": data
            })
        except Exception as e:
            print_error_message(f"Error while receiving blob '{news_record.blob_id}': {e}")
    return json.dumps(all_results, ensure_ascii=False)
