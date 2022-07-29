from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class Genre(models.Base):
    __tablename__ = 'genres'
    name = Column(String(100), unique=True, nullable=False)


class Director(models.Base):
    __tablename__ = 'directors'
    name = Column(String(100), unique=True, nullable=False)


class Movie(models.Base):
    __tablename__ = 'movies'
    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(100), unique=True, nullable=False)
    trailer = Column(String(100), unique=True, nullable=False)
    year = Column(Integer, unique=False, nullable=False)
    rating = Column(Float, unique=False, nullable=False)
    genre_id = Column(Integer, ForeignKey(f'{Genre.__tablename__}.id'), unique=False, nullable=False)
    director_id = Column(Integer, ForeignKey(f'{Director.__tablename__}.id'), unique=False, nullable=False)
    genre = relationship("Genre")
    director = relationship("Director")


class User(models.Base):
    __tablename__ = 'users'

    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), unique=False, nullable=False)
    name = Column(String(255))
    surname = Column(String(255))
    favorite_genre = Column(Integer, ForeignKey(f'{Genre.__tablename__}.id'))
    favorite_genre_rel = relationship("Genre")


class FavoriteMovie(models.Base):
    __tablename__ = 'favorite_movie'
    user_id = Column(Integer, ForeignKey(f'{User.__tablename__}.id'))
    movie_id = Column(Integer, ForeignKey(f'{Movie.__tablename__}.id'))
    user_idr = relationship("User")
    movie_idr = relationship("Movie")
