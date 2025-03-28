from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CommentDTO(BaseModel):
    comment_id: Optional[int] = Field(None)
    user_id: Optional[int] = Field(None)
    news_id: Optional[int] = Field(None)
    timestamp: Optional[datetime] = Field(None)
    content: Optional[str] = Field(None)
    parent_comment_id: Optional[int] = Field(None)

    class Config:
        from_attributes = True

