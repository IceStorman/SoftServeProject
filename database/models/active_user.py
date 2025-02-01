from datetime import datetime, timedelta

from .base import Base, Column, DateTime, String


class ActiveUser(Base):
    __tablename__ = 'active_users'
    user_id = Column(String, primary_key=True)
    last_seen = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # def is_expired(self):
    #     return datetime.utcnow() - self.last_seen > timedelta(hours=3)