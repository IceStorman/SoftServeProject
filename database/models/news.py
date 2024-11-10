from .base import Base, Column, Integer, String

class News(Base):
    __tablename__ = 'News'
    news_id = Column(Integer, primary_key=True)
    blob_id = Column(String)
    interest_rate = Column(Integer)
