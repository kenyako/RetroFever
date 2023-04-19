import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class GenreFilm(SqlAlchemyBase):
    __tablename__ = 'genres_films'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
