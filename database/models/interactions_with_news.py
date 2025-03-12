from .base import Base, Column, Integer, ForeignKey, String, DateTime

class InteractionWithNews(Base):
    __tablename__ = 'InteractionsWithNews'
    interaction_id = Column(Integer, primary_key=True)
    news_id = Column(ForeignKey('News.news_id'))
    user_id = Column(ForeignKey('Users.user_id'))
    type_of_interaction = Column(ForeignKey('InteractionTypes.interaction_type_id'))
    timestamp = Column(DateTime)