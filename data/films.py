import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Films(SqlAlchemyBase):
    __tablename__ = 'films'

    id = sqlalchemy.Column(
        sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(
        'genres_films.id'), nullable=True)
    duration = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    budget = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    premiere = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    director = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    production = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    info = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # genre_film = orm.relationship('GenreFilm', back_populates='films')
