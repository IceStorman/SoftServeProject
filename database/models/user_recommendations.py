from .base import Base, Column, Integer, String, ForeignKey, Float

class UserNewsRecommendations(Base):
    __tablename__ = 'User_recommendations'
    user_recommendations_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.user_id'))
    news_id = Column(Integer, ForeignKey('News.news_id'))
    score = Column(Float)
    rating = Column(Integer)