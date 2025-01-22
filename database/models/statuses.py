from .base import Base, Column, Integer, String, ForeignKey, Boolean

class Statuses(Base):
    __tablename__ = 'Statuses'
    status_id = Column(Integer, primary_key=True)
    status_name=Column(String)
    