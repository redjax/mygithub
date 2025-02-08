import typing as t
from .models import GithubStarsAPIResponseModel
from mygh.libs import db_lib
import sqlalchemy as sa
import sqlalchemy.orm as so
import sqlalchemy.exc as sa_exc


class GithubStarsAPIResponseRepository(db_lib.base.BaseRepository[GithubStarsAPIResponseModel]):
    def __init__(self, session: so.Session):
        super().__init__(session, GithubStarsAPIResponseModel)