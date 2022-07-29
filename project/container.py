from project.dao import GenresDAO, MoviesDAO, UsersDAO, DirectorsDAO, FavoritesDAO

from project.services import GenresService, MoviesService, UsersService, DirectorsService
from project.services.auth_service import AuthService
from project.services.favorites_movie_service import FavoritesMovieService
from project.setup.db import db

# DAO
genre_dao = GenresDAO(db.session)
director_dao = DirectorsDAO(db.session)
movie_dao = MoviesDAO(db.session)
user_dao = UsersDAO(db.session)
favorite_movie_dao = FavoritesDAO(db.session)

# Services
genre_service = GenresService(dao=genre_dao)
director_service = DirectorsService(dao=director_dao)
movie_service = MoviesService(dao=movie_dao)
user_service = UsersService(dao=user_dao)
auth_service = AuthService(dao=user_dao)
favorite_movie_service = FavoritesMovieService(dao=favorite_movie_dao)
