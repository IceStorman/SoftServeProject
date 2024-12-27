from .base import Base, Column, Integer, String, ForeignKey
from typing import Dict
from database.session import SessionLocal

class Country(Base):
    __tablename__ = 'Country'
    country_id = Column(Integer, primary_key=True)
    flag = Column(String)
    sport_id = Column(ForeignKey('Sports.sport_id'))
    name = Column(String)
    code = Column(String)
    api_id = Column(Integer)

    def __init__(self, json_data: Dict):
        for column in self.__table__.columns:
            if column.name in json_data:
                setattr(self, column.name, json_data[column.name])

    def save(self):
        session = SessionLocal()
        existing_record = session.query(type(self)).filter_by(name=self.name).first()
        if existing_record:
            for attr, value in self.__dict__.items():
                if attr != "_sa_instance_state":  # пропустити службовий атрибут SQLAlchemy
                    setattr(existing_record, attr, value)
        else:
            session.add(self)
        session.commit()
        # виправити
        self.country_id = session.query(type(self)).filter_by(name=self.name).first().country_id