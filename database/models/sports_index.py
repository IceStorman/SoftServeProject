from .base import Base, Column, Integer, ForeignKey, String

class SportIndex(Base):
    __tablename__ = 'SportsIndex'
    index_id = Column(Integer, primary_key=True)
    sport_id = Column(ForeignKey('Sports.sport_id'))