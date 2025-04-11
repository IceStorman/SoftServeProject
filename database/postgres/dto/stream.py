from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

class StreamDTO(BaseModel):
    stream_id: Optional[int] = None
    title: str
    start_time: Optional[datetime] = None
    sport_id: int
    stream_urls: Optional[List[str]] = None

    model_config = {"from_attributes": True}


class StreamStatusDTO(BaseModel):
    streams_status_id: Optional[int] = None
    status_id: Optional[int] = None
    stream_id: Optional[int] = None

    model_config = {"from_attributes": True}


class StreamUrlDTO(BaseModel):
    streams_url_id: Optional[int] = None
    stream_id: int
    stream_url: str

    model_config = {"from_attributes": True}