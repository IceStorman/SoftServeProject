from .base import Base, Column, Integer, ForeignKey

class UserPreference(Base):
    __tablename__ = 'UserPreferences'
    user_pref_id = Column(Integer, primary_key=True)
    sports_id = Column(ForeignKey('Sports.sport_id'))
    users_id = Column(ForeignKey('Users.user_id'))