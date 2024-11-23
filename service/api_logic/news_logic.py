import json
from database.models import News, Sport
from database.azure_blob_storage.save_get_blob import blob_get_news
from exept.colors_text import print_error_message


def get_news_by_count(count: int, session) -> str:
    news_records = session.query(News).order_by(News.save_at.desc()).limit(count).all()
    if not news_records:
        print_error_message(f"No news was found in the database.")
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


def get_latest_sport_news(count: int, sport_name, session):
    sport = session.query(Sport).filter(Sport.sport_name == sport_name).first()
    if not sport:
        return {"error": f"Sport '{sport_name}' not found"}
    news_records = (
        session.query(News).filter(News.sport_id == sport.sport_id)
        .order_by(News.save_at.desc()).limit(count).all()
    )

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


