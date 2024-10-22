import json

from flask import request
from flask_restx import Namespace, Resource, fields

import toy.services.example_services as example_services

example_ns = Namespace(name='example', path='/1.0', description='This api is Example for first')
# 따로 path가 없으면 name이 해당 prefix가 된다.

"""
스키마 정의
"""
example_create_model = example_ns.model('create', {
    'name': fields.String
})


# https://sepang2.tistory.com/113
"""
class _Schema():
    post_fields = ns.model('컨테이너 생성시 필요 데이터', {
        'description': fields.String(description='Container Description', example='Container for tag management'),
        'domain': fields.String(description='Domain of the Container', example='samsung.com')
    })
    basic_fields = ns.model('컨테이너 기본 정보', {
        'description': fields.String(description='Container Name', example='test-container-1'),
        'domain': fields.String(description='Domain of the Container', example='samsung.com')
    })
    detail_fields = ns.model('컨테이너 상세 정보', {
        'description': fields.String(description='Container Description', example='Container for tag management')
    })
    msg_fields = ns.model('상세 코드에 따른 설명', {
        'msg': fields.String(description='상태 코드에 대한 메세지', example='처리 내용')
    })
    container_list = fields.List(fields.Nested(basic_field))
    
    
    사용법: _Schema.container_list
    _Schema.msg_fields
"""


@example_ns.route('/name/<name>')   # 최종은 '/api/1.0/name/<name>' 이 됨
class ExampleRouteGetId(Resource):
    def get(self, name: str) -> json:
        result = example_services.example_route_get_id(name)
        # if result == "":
        #     return {'message': '실패', 'result':'not found'}, 200
        return {'message': '성공',
                'result': result}, 200


@example_ns.route('/create')
# @ns.param('name', 'Create User')  # route: queryString <-- post랑 안 맞음
class ExampleRouteCreate(Resource):
    @example_ns.expect(example_create_model, validate=True)  # post body 입력받음
    @example_ns.marshal_with(example_create_model)
    def post(self) -> json:
        result = example_services.example_route_create(request.data)
        # return {'message': '성공'}, 200
        return {'name': result}, 200


@example_ns.route('/hello')
class ExampleRoute(Resource):
    def get(self) -> dict[str, str]:
        """return hello world"""
        data = 'hello_world'
        result = example_services.example_route(data=data)
        return {"result": result}


@example_ns.route('/<int:user_number>')  # route: pathVariable <type:name>
@example_ns.doc(params={'user_number': '파라미터로 입력된 숫자'})  # params= description
@example_ns.header('content-type', 'application/json')
class ExampleRouteAddParam(Resource):
    @example_ns.response(200, description='입력 받은 파라미터를 제곱하여 반환한다')
    def get(self, user_number: int) -> dict[str, int]:
        """return parameter calculator"""
        result = example_services.example_route_add_param(data=user_number)
        return {"result": result}
