from .base import Column, Integer, ForeignKey, String

from database.models import Base

class TempSubscribers(Base):
    __tablename__ = "TempSubscribersData"
    id = Column(Integer, primary_key=True)
    team_ids = Column(ForeignKey("TeamIndex.team_index_id"))
    subscriber_emails = Column(String)