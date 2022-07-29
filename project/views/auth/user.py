from flask import request
from flask_restx import Namespace, Resource

from project.container import user_service
from project.services.auth_service import auth_required
from project.setup.api.models import user
from project.tools.security import generate_password_hash, compose_passwords

api = Namespace('user')


@api.route('/')
class UserView(Resource):
    @auth_required
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    def get(self):
        """
        Get user by token.
        """
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace("Bearer ", "")
        user = user_service.get_user_by_token(token)
        print(user_service.get_item(user.id))
        return user_service.get_item(user.id)

    @api.marshal_with(user, as_list=True, code=201, description='OK')
    @auth_required
    def patch(self):
        rq_json = request.json
        print(f"rq_json: {rq_json}")
        print(f"request.headers: {request.headers}")
        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace("Bearer ", "")

        email = rq_json.get("email")
        name = rq_json.get("name")
        surname = rq_json.get("surname")
        favorite_genre_id = rq_json.get("favourite_genre")
        print(type(favorite_genre_id))
        print(type(rq_json.get("favorite_genre_id")))
        new_user = user_service.get_user_by_token(token)
        if "email" in rq_json:
            new_user.email = email
        if "name" in rq_json:
            new_user.name = name
        if "surname" in rq_json:
            new_user.surname = surname
        if "favourite_genre" in rq_json:
            new_user.favorite_genre = favorite_genre_id
            print("Отработал")
        user_service.partial_update(new_user)

@api.route('/password/')
class UserView(Resource):
    @api.marshal_with(user, as_list=True, code=201, description='OK')
    @api.response(404, 'Not Found')
    @auth_required
    def put(self):
        rq_json = request.json

        token = request.headers.environ.get('HTTP_AUTHORIZATION').replace("Bearer ", "")
        old_password = rq_json.get("password_1")
        new_password = rq_json.get("password_2")

        user_with_new_password = user_service.get_user_by_token(token)
        if compose_passwords(user_with_new_password.password, old_password):
            user_with_new_password.password = generate_password_hash(new_password)
            user_service.partial_update(user_with_new_password)
            return "Пароль успешно изменен!", 200
        return "Старый пароль неверен", 400

