from .base import Base, Column, Integer, String, ForeignKey, Boolean, DateTime

class Stream(Base):
    __tablename__ = 'Streams'
    stream_id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    sport_id = Column(ForeignKey('Sports.sport_id'))
    title = Column(String)