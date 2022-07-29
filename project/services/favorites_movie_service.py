from typing import Optional

import jwt
from flask import current_app

from project.dao import FavoritesDAO
from project.exceptions import ItemNotFound
from project.models import FavoriteMovie


class FavoritesMovieService:
    def __init__(self, dao: FavoritesDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> FavoriteMovie:
        if favoritemovie := self.dao.get_by_id(pk):
            return favoritemovie
        raise ItemNotFound(f'Favorite movie with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[FavoriteMovie]:
        return self.dao.get_all(page=page)

    def add_movie(self, user_id, movie_id):
        self.dao.add_new(user_id, movie_id)

    def delete_movie(self, idf):
        self.dao.delete(idf)

