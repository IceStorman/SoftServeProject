from .base import Base, Column, Integer, String, ForeignKey

class Players(Base): # For players in formula-1 and mma
    __tablename__ = 'Players'
    player_id = Column(Integer, primary_key=True)
    api_id = Column(Integer)
    name = Column(String)
    logo = Column(String)
    team_index_id = Column(ForeignKey('TeamIndex.team_index_id'))
    sport_id = Column(ForeignKey('Sports.sport_id'))