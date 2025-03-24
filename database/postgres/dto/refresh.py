from marshmallow import Schema, fields, validate
import re

def validate_ip(value):
    pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if not pattern.match(value):
        raise ValueError("Invalid IP address format")
    
    octets = value.split(".")
    if any(int(octet) > 255 or int(octet) < 0 for octet in octets):
        raise ValueError("IP address octets must be between 0-255")

class RefreshTokenDTO(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    last_ip = fields.Str(required=True, validate=validate_ip)
    last_device = fields.Str(required=True)
    nonce = fields.Str(required=True)