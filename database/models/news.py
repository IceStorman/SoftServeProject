from .base import Base, Column, Integer, String, DateTime, ForeignKey

class News(Base):
    __tablename__ = 'News'
    news_id = Column(Integer, primary_key=True)
    blob_id = Column(String)
    sport_id = Column(ForeignKey('Sports.sport_id'))
    interest_rate = Column(Integer)
    save_at = Column(DateTime)
