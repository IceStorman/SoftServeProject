from marshmallow import Schema, fields
from typing import Optional
import datetime

class RefreshTokenDTO(Schema):
    id: Optional[int] = fields.Int(default=None)
    user_id: int = fields.Int(...)
    last_ip: str = fields.Strtr(...)
    last_device: str = fields.Str(...)
    nonce: str = fields.Str(...)

    class Config: 
        
        from_attributes = True