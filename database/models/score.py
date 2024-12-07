from .base import Base, Column, Integer, ForeignKey

class Score(Base):
    __tablename__ = 'Score'
    score_id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey('Game.game_id'))
    away = Column(Integer)
    home = Column(Integer)
