from loguru import logger as log
import typing as t
from datetime import datetime

from pydantic import BaseModel, Field, field_validator, ValidationError, computed_field

class GithubStarsAPIResponseBase(BaseModel):
    json_data: t.List[t.Dict[str, t.Any]] = Field(default_factory=[], repr=False)
    
    @computed_field
    @property
    def stars_count(self) -> int:
        if self.json_data:
            return len(self.json_data)
        else:
            return 0
    
class GithubStarsAPIResponseIn(GithubStarsAPIResponseBase):
    pass

class GithubStarsAPIResponseOut(GithubStarsAPIResponseBase):
    id: int

    created_at: datetime
    updated_at: datetime
