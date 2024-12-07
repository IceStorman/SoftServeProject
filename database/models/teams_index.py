from .base import Base, Column, Integer, String, ForeignKey

class TeamIndex(Base):
    __tablename__ = 'TeamIndex'
    team_index_id = Column(Integer, primary_key=True)
    news_id = Column(ForeignKey('News.news_id'))
    sport_id = Column(ForeignKey('Sport.sport_id'))
    name = Column(String)
    logo = Column(String)
    api_id = Column(Integer)
    country = Column(ForeignKey('Country.country_id'))
