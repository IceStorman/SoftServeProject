from .base import Base, Column, Integer, String, ForeignKey

class TeamIndex(Base):
    __tablename__ = 'TeamIndex'
    team_index_id = Column(Integer, primary_key=True)
    sport_id = Column(ForeignKey('Sports.sport_id'))
    name = Column(String)
    logo = Column(String)
    api_id = Column(Integer)
    league = Column(ForeignKey('League.league_id'))