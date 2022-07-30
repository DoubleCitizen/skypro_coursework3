from flask_restx import Namespace, Resource
from flask import request, jsonify
from project.container import user_service, auth_service
from project.setup.api.models import user

api = Namespace('auth')


@api.route('/register/')
class RegisterView(Resource):
    @api.marshal_with(user, as_list=True, code=201, description='Created')
    def post(self):
        rq_json = request.json
        login = rq_json.get('email')
        password = rq_json.get('password')

        if login and password:
            user_service.create_user(login, password), 201
        else:
            return "Не хватает пароля или почты", 401


@api.route('/login/')
class LoginView(Resource):
    @api.marshal_with(user, as_list=True, code=200, description='OK')
    @api.response(404, 'Not Found')
    def post(self):
        rq_json = request.json
        login = rq_json.get('email')
        password = rq_json.get('password')

        if login and password:
            try:
                return auth_service.check(login, password), 201
            except Exception as e:
                print(e)
                return "", 400

    @api.marshal_with(user, as_list=True, code=201, description='OK')
    @api.response(404, 'Not Found')
    def put(self):
        rq_json = request.json
        access_token = rq_json.get('access_token')
        refresh_token = rq_json.get('refresh_token')
        if access_token and refresh_token:
            return auth_service.approve_refresh_token(refresh_token), 201
