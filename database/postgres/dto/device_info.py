from pydantic import BaseModel, Field
from typing import Optional
import datetime

class DeviceInfoDTO(BaseModel):
    browser: str = Field(...)
    os : str = Field(...)
    device: str = Field(...)

    class Config: 
        
        from_attributes = True