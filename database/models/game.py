from .base import Base, Column, Integer, String, ForeignKey

class Games(Base):
    __tablename__ = 'Games'
    game_id = Column(Integer, primary_key=True)
    league_id = Column(ForeignKey('League.league_id'))
    sport_id = Column(ForeignKey('Sports.sport_id'))
    country_id = Column(ForeignKey('Country.country_id'))
    team_away_id = Column(ForeignKey('TeamIndex.team_index_id'))
    team_home_id = Column(ForeignKey('TeamIndex.team_index_id'))
    score_away_team = Column(Integer)
    score_home_team = Column(Integer)
    status = Column(String)
    type = Column(ForeignKey('GamesStatuses.game_status_id'))
    time = Column(String)
    date = Column(String)
    api_id = Column(Integer)