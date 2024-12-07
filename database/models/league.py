from .base import Base, Column, Integer, ForeignKey, String

class League(Base):
    __tablename__ = 'League'
    legue_id = Column(Integer, primary_key=True)
    api_id = Column(Integer)
    name = Column(String)
    logo = Column(String)
    sport_id = Column(ForeignKey('Sports.sport_id'))