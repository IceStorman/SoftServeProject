from .base import Base, Column, Integer, ForeignKey, String

class StreamUrl(Base):
    __tablename__ = 'StreamUrl'
    stream_url_id = Column(Integer, primary_key=True)
    stream_id = Column(ForeignKey('Streams.stream_id'))
    stream_url = Column(String)