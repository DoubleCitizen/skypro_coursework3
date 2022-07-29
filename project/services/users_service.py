import base64
import hashlib
from typing import Optional

import jwt
from flask import current_app

from project.dao import UsersDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import generate_password_hash, compose_passwords


class UsersService:
    def __init__(self, dao: UsersDAO) -> None:
        self.dao = dao

    def get_item(self, pk: int) -> User:
        if user := self.dao.get_by_id(pk):
            return user
        raise ItemNotFound(f'User with pk={pk} not exists.')

    def get_all(self, page: Optional[int] = None) -> list[User]:
        return self.dao.get_all(page=page)

    def get_user_by_login(self, login):
        return self.dao.get_user_by_login(login)

    def create_user(self, login, password):
        self.dao.create(login, generate_password_hash(password))

    def partial_update(self, user_d):
        return self.dao.partial_update(user_d)

    def get_user_by_token(self, token):
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[current_app.config["ALGORITHM"]])
        return self.get_user_by_login(data['login'])
