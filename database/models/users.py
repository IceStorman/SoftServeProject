from .base import Base, Column, Integer, String

class User(Base):
    __tablename__ = 'Users'
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)
    sport_pref_key = Column(Integer)
    club_pref_key = Column(Integer)
    theme = Column(String)