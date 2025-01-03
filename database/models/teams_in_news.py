from .base import Base, Column, Integer, String, ForeignKey

class TeamInNews(Base):
    __tablename__ = 'TeamInNews'
    team_id = Column(Integer, primary_key=True)
    news_id = Column(ForeignKey('News.news_id'))
    name = Column(String)
    team_index_id = Column(ForeignKey('TeamIndex.team_index_id'))