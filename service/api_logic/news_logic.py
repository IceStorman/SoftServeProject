import json
from flask import Response
from sqlalchemy import desc
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
        self._logger = Logger("logger", "all.log").logger
    

    def get_news_by_count(self, COUNT: int):
        news = self._news_dal.fetch_news(order_by=desc(News.save_at), limit=COUNT)
        return self.json_news(news)



    def get_latest_sport_news(self, count: int, sport_name: str):
        sport = self._news_dal.get_sport_by_name(sport_name)
        #sport = get_sport_by_name(self.session, sport_name)
        filters = [News.sport_id == sport.sport_id]
        news = self._news_dal.fetch_news(order_by=desc(News.save_at), limit=COUNT, filters=filters)
        return self.json_news(news)

    def get_popular_news(self, COUNT: int):
        news = self._news_dal.fetch_news(order_by=desc(News.interest_rate), limit=COUNT)
        return self.json_news(news)


    def get_news_by_id(self, blob_id: str):
        news = self._news_dal.get_news_by_blob_id(blob_id)
        if news:
            self._logger.warning(f"News were found: {news}")
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

    async def send_all_info_from_blob_to_user(self, recommendations_list):
        all_news_from_blob = []
        for recs in recommendations_list:
            news_id = recs["news_id"]
            news_from_blob = self._news_dal.get_news_by_id(news_id)
            all_news_from_blob.append(news_from_blob)

        return self.json_news(all_news_from_blob)

