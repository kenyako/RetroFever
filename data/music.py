import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Music(SqlAlchemyBase):
    __tablename__ = 'music'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)

    track_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    period = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    path = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
