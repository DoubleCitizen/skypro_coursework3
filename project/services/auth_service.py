import calendar
import datetime
from typing import Optional

import jwt
from flask import current_app, request, abort

from project.dao import UsersDAO
from project.exceptions import ItemNotFound
from project.models import User
from project.tools.security import compose_passwords


def auth_required(func):
    def wrapper(*args, **kwargs):
        try:
            header = request.headers.environ.get('HTTP_AUTHORIZATION').replace("Bearer ", "")
        except Exception as e:
            print(e)
            abort(400)
        if not "Authorization" in request.headers:
            abort(401)

        token = header
        try:
            jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=[current_app.config["ALGORITHM"]])
        except Exception as e:
            print(f"JWT decode error: {e}")
            abort(401)
        return func(*args, **kwargs)

    return wrapper


class AuthService:
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
        return self.dao.create(login, password)

    def generate_tokens(self, login, password, is_refresh=False):
        user = self.get_user_by_login(login)

        if user is None:
            return False

        if not is_refresh:
            if not compose_passwords(user.password, password):
                return False
        data = {
            "login": user.email,
        }

        # access token on 15 min
        min15 = datetime.datetime.utcnow() + datetime.timedelta(minutes=current_app.config['TOKEN_EXPIRE_MINUTES'])
        data["exp"] = calendar.timegm(min15.timetuple())
        access_token = jwt.encode(data, key=current_app.config['SECRET_KEY'], algorithm=current_app.config['ALGORITHM'])

        # refresh token on 130 days
        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, key=current_app.config['SECRET_KEY'],
                                   algorithm=current_app.config['ALGORITHM'])

        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens

    def approve_refresh_token(self, refresh_token):
        data = jwt.decode(refresh_token, current_app.config['SECRET_KEY'], algorithms=[current_app.config['ALGORITHM']])
        login = data["login"]
        user = self.get_user_by_login(login)

        if user is None:
            return False

        return self.generate_tokens(login, user.password, is_refresh=True)

    def check(self, login, password):
        user = self.get_user_by_login(login)
        if user:
            if compose_passwords(user.password, password):
                return self.generate_tokens(user.email, password)
