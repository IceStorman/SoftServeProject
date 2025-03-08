from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class StreamDTO(BaseModel):
    stream_id: Optional[int] = Field(None)
    stream_url: Optional[str] = Field(None)
    start_time: Optional[datetime] = Field(None)
    sport_id: Optional[int] = Field(None)

    class Config:
        from_attributes = True


class StreamStatusDTO(BaseModel):
    streams_status_id: Optional[int] = Field(None)
    status_id: Optional[int] = Field(None)
    stream_url: Optional[str] = Field(None)

    class Config:
        from_attributes = True