import typing as t
from datetime import datetime

from mygh.libs import db_lib
from mygh.libs.depends import db_depends
import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.exc as sa_exc
from sqlalchemy.types import JSON


class GithubStarsAPIResponseModel(db_lib.base.Base):
    __tablename__ = "gh_stars_api_response"
    
    id: so.Mapped[db_lib.annotated.INT_PK]
    
    json_data: so.Mapped[list[dict]] = so.mapped_column(JSON, nullable=False)
    
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now()
    )
    updated_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()
    )