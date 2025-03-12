from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base  

class RefreshTokenTracking(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, ForeignKey("Token_blocklist.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)    
    last_ip = Column(String, nullable=False)  
    last_device = Column(String, nullable=False)
    nonce = Column(String, nullable=False)