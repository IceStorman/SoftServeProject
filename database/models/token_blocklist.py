from .base import Base, Column, Integer, String, ForeignKey, Boolean, DateTime
import datetime 

class TokenBlocklist(Base):
    __tablename__ = 'Token_Blocklist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    jti = Column(String(36), nullable=False, index=True)
    token_type = Column(String(10), nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)  