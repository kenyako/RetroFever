import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Performers(SqlAlchemyBase):
    __tablename__ = 'performers'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    activity = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
