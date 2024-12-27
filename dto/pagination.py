from typing import Optional, Tuple
from pydantic import BaseModel, field_validator

class Pagination(BaseModel):
    page: Optional[int] = 0
    per_page: Optional[int] = 9

    @field_validator("page", "per_page", mode="before")
    def validate_positive(cls, value: Optional[int]) -> Optional[int]:
        if value is not None and value < 0:
            return abs(value)
        return value

    def get_pagination(self) -> Tuple[Optional[int], Optional[int]]:
        if self.page != 0:
            offset = (self.page - 1) * self.per_page
            limit = self.per_page
            return offset, limit
        return None, None
