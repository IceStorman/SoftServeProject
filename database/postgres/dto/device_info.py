from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import datetime

class DeviceInfoDTO(BaseModel):
    browser: str = Field(...)
    os : str = Field(...)
    device: str = Field(...)

    class Config:  
        model_config = ConfigDict(from_attributes=True) 