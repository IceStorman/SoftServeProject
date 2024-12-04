from .base import Base, Column, Integer, String

class Sport(Base):
    __tablename__ = 'Sports'
    sport_id = Column(Integer, primary_key=True)
    sport_name = Column(String)