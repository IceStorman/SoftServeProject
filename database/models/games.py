from .base import Base, Column, Integer, String, ForeignKey

class Games(Base):
    __tablename__ = 'Games'
    game_id = Column(Integer, primary_key=True)
    league_id = Column(ForeignKey('League.legue_id'))
    sport_id = Column(ForeignKey('Sport.sport_id'))
    country_id = Column(ForeignKey('Country.country_id'))
    team_away_id = Column(ForeignKey('TeamIndex.team_index_id'))
    team_home_id = Column(ForeignKey('TeamIndex.team_index_id'))
    status = Column(String)
    time = Column(String)
    date = Column(String)
    api_id = Column(Integer)