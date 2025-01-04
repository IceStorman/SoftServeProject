from .base import Base, Column, Integer, String, ForeignKey, Boolean

class Streams_Status(Base):
    __tablename__ = "Streams_Status"
    stream_id=Column(ForeignKey('Streams.stream_id'), primary_key=True)
    status=Column(String)
    time=Column(Integer)