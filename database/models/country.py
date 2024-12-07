from .base import Base, Column, Integer, String, ForeignKey

class Country(Base):
    __tablename__ = 'Country'
    country_id = Column(Integer, primary_key=True)
    flag = Column(String)
    sport_id = Column(ForeignKey('Sport.sport_id'))
    name = Column(String)
    code = Column(String)
    api_id = Column(Integer)