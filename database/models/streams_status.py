from .base import Base, Column, Integer, String, ForeignKey, Boolean

class Streams_Status(Base):
    __tablename__ = "Streams_Status"
    streams_status_id = Column(Integer, primary_key=True)
    stream_id=Column(ForeignKey('Streams.stream_id'))
    status_id=Column(Integer)