from sqlalchemy import ClauseElement
from database.models import News
from sqlalchemy.orm import Session

class NewsDAL:
    def __init__(self, session = None):
        self.session = session

    def fetch_news(self, order_by=None, limit=None, filters=None):
        query = self.session.query(News)
        
        if filters:
            query = query.filter(*filters)
        
        if order_by is not None:
            if isinstance(order_by, ClauseElement):  
                query = query.order_by(order_by)
            else:
                raise ValueError("Invalid order_by argument. Must be a SQLAlchemy ClauseElement.")
        
        if limit:
            query = query.limit(limit)
        
        return query.all()


    def get_news_by_id(self, blob_id: str):
        return self.session.query(News).filter(News.blob_id == blob_id).first()

    def get_query(self):
        return self.session.query(News)

    def execute_query(self, query):
        return query.all()
