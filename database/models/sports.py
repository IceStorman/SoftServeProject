from .base import Base, Column, Integer, String

class Sport(Base):
    __tablename__ = 'Sports'
    sport_id = Column(Integer, primary_key=True)
    sport_name = Column(String)
    sport_img = Column(String)

    def __init__(self, sport_name):
        self.sport_name = sport_name