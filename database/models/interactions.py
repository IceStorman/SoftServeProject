from .base import Base, Column, Integer, ForeignKey, String

class Interaction(Base):
    __tablename__='Interactions'
    interaction_id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('Users.user_id'))
    news_id = Column(ForeignKey('News.news_id'))
    interaction_type = Column(String)