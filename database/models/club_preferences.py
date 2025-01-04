from .base import Base, Column, Integer, String, ForeignKey

class ClubPreference(Base):
    __tablename__ = 'ClubPreferences'
    pref_id = Column(Integer, primary_key=True)
    users_id = Column(ForeignKey('Users.user_id'))
    preferences = Column(String)