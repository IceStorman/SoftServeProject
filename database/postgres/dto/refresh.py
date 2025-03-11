from marshmallow import Schema, fields
from typing import Optional
import datetime

class RefreshTokenDTO(Schema):
    id = fields.Int(required=False, allow_none=True)
    user_id = fields.Int(required=True)
    last_ip = fields.Str(required=True)
    last_device = fields.Str(required=True)
    nonce = fields.Str(required=True)

    class Meta:
        ordered = True