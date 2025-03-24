from .base import Base, Column, Integer, String, DateTime, ForeignKey

class News(Base):
    __tablename__ = 'News'
    news_id = Column(Integer, primary_key=True)
    blob_id = Column(String)
    sport_id = Column(ForeignKey('Sports.sport_id'))
    save_at = Column(DateTime)
    likes = Column(Integer, default=0)
    views = Column(Integer, default=0)
