# from marshmallow import Schema, fields, validate
# import re

# def validate_ip(value):
#     pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
#     if not pattern.match(value):
#         raise ValueError("Invalid IP address format")
    
#     octets = value.split(".")
#     if any(int(octet) > 255 or int(octet) < 0 for octet in octets):
#         raise ValueError("IP address octets must be between 0-255")

from pydantic import BaseModel, Field
from typing import Optional
import datetime

class RefreshTokenDTO(BaseModel):
    id: Optional[int] = Field(default=None)
    user_id: int = Field(...)
    last_ip: str = Field(...)
    last_device: str = Field(...)
    nonce: str = Field(...)