from sqlalchemy import desc
from database.models import News, Sport
from sqlalchemy.orm import Session

class NewsDAL:
    def __init__(self, session = None):
        self.session = session

    def fetch_news(self, order_by=None, limit=None, filters=None):
        query = self.session.query(News)
        if filters:
            query = query.filter(*filters)
        if order_by:
            query = query.order_by(order_by)
        if limit:
            query = query.limit(limit)
        return query.all()

    def get_news_by_blob_id(self, blob_id: str):
        return self.session.query(News).filter(News.blob_id == blob_id).first()

    def get_news_by_id(self, news_id: str):
        return self.session.query(News).filter(News.news_id == news_id).first()

    def get_sport_by_name(self, sport_name):
        return self.session.query(Sport).filter_by(sport_name = sport_name).first()

