import json
from database.models import News
from database.azure_blob_storage.save_get_blob import blob_get_news


def get_news_by_count(count: int, session) -> str:
    news_records = session.query(News).order_by(News.save_at.desc()).limit(count).all()
    if not news_records:
        print(f"\033[31mNo news was found in the database.\033[0m")
        return json.dumps([])
    all_results = []
    for news_record in news_records:
        try:
            data = blob_get_news(news_record.blob_id)
            all_results.append({
                "blob_id": news_record.blob_id,
                "data": data
            })
        except Exception as e:
            print(f"\033[31mError while receiving blob '{news_record.blob_id}': {e}\033[0m")
    return json.dumps(all_results, ensure_ascii=False)
