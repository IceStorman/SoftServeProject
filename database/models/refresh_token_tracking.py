from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base  

class refresh_token_tracking(Base):
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, ForeignKey("Token_blocklist.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"), nullable=False)    
    last_ip = Column(String, nullable=False)  
    last_device = Column(String, nullable=False)
    nonce = Column(String, nullable=False)

    refresh_token = relationship("Token_blocklist", backref="refresh_token", foreign_keys=[id])