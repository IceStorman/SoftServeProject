from .base import Base, Column, Integer, String, ForeignKey

class GamesStatuses(Base):
    __tablename__ = 'GamesStatuses'
    game_status_id = Column(Integer, primary_key=True)
    status = Column(String)