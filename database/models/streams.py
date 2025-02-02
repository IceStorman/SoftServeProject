from .base import Base, Column, Integer, String, ForeignKey, Boolean

class Stream(Base):
    __tablename__ = 'Streams'
    stream_id = Column(Integer, primary_key=True)
    stream_url = Column(String) 
    start_time=Column(Integer)
    sport_id = Column(ForeignKey('Sports.sport_id'))