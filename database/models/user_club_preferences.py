from .base import Base, Column, Integer, ForeignKey

class UserClubPreferences(Base):
    __tablename__ = 'UserClubPreferences'
    pref_id = Column(Integer, primary_key=True)
    users_id = Column(ForeignKey('Users.user_id'))
    preferences = Column(ForeignKey('TeamIndex.team_index_id'))