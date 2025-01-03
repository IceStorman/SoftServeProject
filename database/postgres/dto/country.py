from pydantic import BaseModel, Field
from typing import Optional

class CountryDTO(BaseModel):
    country_id: Optional[int] = Field(None)
    flag: Optional[str] = Field(None)
    name: str = Field(...)
    code: Optional[str] = Field(None)
    api_id: Optional[int] = Field(None)

    class Config:
        from_attributes = True
