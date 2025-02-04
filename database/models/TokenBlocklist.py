from .base import Base, Column, Integer, String, ForeignKey, Boolean, DateTime
import datetime

class TockenBlocklist(Base):
    __tablename__ = 'TokenBlocklist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    jti = Column(String(36), nullable=False, index=True)
    token_type = Column(String(10), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  

