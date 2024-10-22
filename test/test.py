from flask_restx import fields

from toy.controllers.example_controllers import ns


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
    container_list = fields.List(fields.Nested(basic_fields))


"""
{
  "containers": [
    {
      "description": "test-container-1",
      "domain": "samsung.com"
    },
    {
      "description": "test-container-2",
      "domain": "example.com"
    }
  ]
}
"""
print(_Schema.basic_fields)
print("")
print(_Schema.container_list)