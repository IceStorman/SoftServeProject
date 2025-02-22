from .base import Base, Column, Integer, ForeignKey, String

class TempSubscribersData(Base):
    __tablename__ = "TempSubscribersData"
    id = Column(Integer, primary_key=True)
    team_ids = Column(ForeignKey("TeamIndex.team_index_id"))
    subscriber_emails = Column(String)