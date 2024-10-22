import json

from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import Namespace, fields, Resource

from toy.services import example_services, sign_services

sign_ns = Namespace(name='sign', path='/1.0', description='sign_ns')
# 따로 path가 없으면 name이 해당 prefix가 된다.

example_create_model = sign_ns.model('create', {
    'name': fields.String
})
example_sign_up_model = sign_ns.model('sign-up', {
    'user_id': fields.String(required=True),
    'password': fields.String(required=True),
})

example_login_model = sign_ns.model('login', {
    'user_id': fields.String(required=True),
    'password': fields.String(required=True),
})


@sign_ns.route('/signup')
class ExampleSingUp(Resource):
    @sign_ns.expect(example_sign_up_model)
    def post(self):
        result = sign_services.example_sign_up(request.data)
        return result, 200


@sign_ns.route('/login')
class ExampleLogin(Resource):
    @sign_ns.expect(example_login_model)
    def post(self) -> json:
        result = sign_services.example_login(request.data)
        return result


@sign_ns.route('/logout')
class ExampleLogout(Resource):
    @jwt_required()
    def delete(self):
        return sign_services.example_logout()


@sign_ns.route('/refresh')
class ExampleRefresh(Resource):
    @jwt_required(refresh=True)
    def get(self):
        return sign_services.example_refresh()