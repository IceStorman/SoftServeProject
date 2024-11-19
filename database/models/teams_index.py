from .base import Base, Column, Integer, String, ForeignKey

class TeamIndex(Base):
    __tablename__ = 'TeamIndex'
    team_index_id = Column(Integer, primary_key=True)
    news_id = Column(ForeignKey('News.news_id'))
    team_name = Column(String)