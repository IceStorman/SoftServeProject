from .base import Base, Column, Integer, ForeignKey, String

class League(Base):
    __tablename__ = 'League'
    league_id = Column(Integer, primary_key=True)
    api_id = Column(Integer)
    name = Column(String)
    logo = Column(String)
    sport_id = Column(ForeignKey('Sports.sport_id'))
    country = Column(ForeignKey('Country.country_id'))