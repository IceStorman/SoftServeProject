from .base import Base, Column, Integer, ForeignKey, String

class Views(Base):
    __tablename__ = 'Views'
    views_id = Column(Integer, primary_key=True)
    news_id = Column(ForeignKey('News.news_id'))
    users_id = Column(ForeignKey('Users.user_id'))
    timestamp = Column(String)