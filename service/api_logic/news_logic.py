import json
from flask import Response
from database.models import News
from database.azure_blob_storage.save_get_blob import blob_get_news
from sqlalchemy.sql.expression import ClauseElement
from exept.handle_exeptions import handle_exceptions
from service.api_logic.scripts import get_sport_by_name
from database.session import SessionLocal
from logger.logger import Logger


class NewsService:
    def __init__(self, news_dal):
        self._news_dal = news_dal
        self.logger = Logger("logger", "all.log").logger
    

    def get_news_by_count(self, count: int):
        news = self._news_dal.fetch_news(order_by=News.save_at.desc(), limit=count)
        return self.json_news(news)


    def get_latest_sport_news(self, count: int, sport_name: str):
        sport = get_sport_by_name(self.session, sport_name)
        filters = [News.sport_id == sport.sport_id]
        news = self._news_dal.fetch_news(order_by=News.save_at.desc(), limit=count, filters=filters)
        return self.json_news(news)


    def get_popular_news(self, count: int):
        news = self._news_dal.fetch_news(order_by=News.interest_rate.desc(), limit=count)
        return self.json_news(news)


    def get_news_by_id(self, blob_id: str):
        news = self._news_dal.get_news_by_id(blob_id)
        if news:
            self.logger.warning(f"News were found: {news}")
            return self.json_news([news])

    def json_news(self, news_records):
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

