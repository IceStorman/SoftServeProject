from .country import Country
from .base import Base, Column, Integer, String, ForeignKey
from typing import Dict
from database.session import SessionLocal

class TeamIndex(Base):
    __tablename__ = 'TeamIndex'
    team_index_id = Column(Integer, primary_key=True)
    news_id = Column(ForeignKey('News.news_id'))
    sport_id = Column(ForeignKey('Sports.sport_id'))
    name = Column(String)
    logo = Column(String)
    api_id = Column(Integer)
    country = Column(ForeignKey('Country.country_id'))
    league = Column(ForeignKey('League.league_id'))

    def __init__(self, json_data: Dict, sport_id: int):
        self.sport_id = sport_id
        setattr(self, 'api_id', json_data['id'])
        for column in self.__table__.columns:
            if column.name in json_data:
                if column.name == 'country':
                    country_entry = Country(json_data[column.name])
                    country_entry.save()
                    setattr(self, column.name, country_entry.country_id)
                else:
                    setattr(self, column.name, json_data[column.name])

    def save(self):
        session = SessionLocal()
        existing_record = session.query(type(self)).filter_by(api_id=self.api_id, sport_id=self.sport_id).first()
        if existing_record:
            for attr, value in self.__dict__.items():
                if attr != "_sa_instance_state":  # пропустити службовий атрибут SQLAlchemy
                    setattr(existing_record, attr, value)
        else:
            session.add(self)
        session.commit()