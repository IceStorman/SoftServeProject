from .base import Base, Column, Integer, String, ForeignKey

class BlobIndex(Base):
    __tablename__ = 'BlobIndex'
    blob_id = Column(Integer, primary_key=True)
    sports_index_id = Column(ForeignKey('SportsIndex.index_id'))
    filename = Column(String)
