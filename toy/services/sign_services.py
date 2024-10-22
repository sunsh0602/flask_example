from flask import json
from flask import jsonify
from flask import request

from datetime import datetime
from datetime import timedelta
from datetime import timezone

from toy import bcrypt
from toy import jwt_redis

from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import get_jwt_header
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import set_refresh_cookies
from flask_jwt_extended import unset_jwt_cookies

from toy.daos.example_dao import ExampleDAO
from toy.daos.example_dao import ExampleSignDAO
from toy.daos.example_dao import ExampleRefreshDAO


# 회원가입
def example_sign_up(data: bytes) -> json:
    user = json.loads(data)
    user_id = user['user_id']
    # password를 bcrypt로 암호화 하고 저장한다.
    pw_hash = bcrypt.generate_password_hash(user['password'])
    dao = ExampleSignDAO()
    dao.create(user_id=user_id, password=pw_hash)

    return {"result": "success"}


# 로그인
def example_login(data: bytes) -> json:
    user = json.loads(data)
    user_id = user['user_id']
    password = user['password']

    # 로그인
    dao = ExampleSignDAO()
    dao.get(user_id=user_id, password=password)

    response = jsonify({"msg": "login successful"})

    # token 생성
    access_token = create_access_token(identity=user_id)
    refresh_token = create_refresh_token(identity=user_id)

    # cookie 설정
    set_access_cookies(response=response, encoded_access_token=access_token)
    set_refresh_cookies(response=response, encoded_refresh_token=refresh_token)

    # redis에 설정
    jwt_redis.set(refresh_token, user_id, ex=timedelta(days=14))
    return response


# 로그아웃
def example_logout() -> json:
    response = jsonify({"msg": "logout successful"})

    # redis에 저장되어 있는 refresh token 삭제
    jwt_redis.delete(request.cookies.get('refresh_token_cookie'))

    # jwt로 생성된 cookie 전체 삭제
    unset_jwt_cookies(response)
    return response


# jwt tokent refresh
def example_refresh():
    # request에서 cookie를 가져온다.
    token = request.cookies.get('refresh_token_cookie')

    # refresh token이 redis에 존재 여부 확인
    is_tk = jwt_redis.get(token)

    # refresh token에 있는 user_id가 유저가 맞는지 확인
    is_user_id = ExampleRefreshDAO()

    # redis에 refresh token이 없는 경우 or 로그인아이디가 DB에 없는 경우
    if is_tk is None or is_user_id.get(get_jwt_identity()) is None:
        return {'msg': 'refresh failed'}, 400

    # access token 재발급
    user_id = get_jwt_identity()
    response = jsonify({"msg": "refresh successful"})
    access_token = create_access_token(identity=user_id)
    set_access_cookies(response=response, encoded_access_token=access_token)

    # refresh token의 expire 시간이 10시간 이하일 경우 refresh token 재발급
    exp_timestamp = get_jwt()['exp']
    now = datetime.now(timezone.utc)
    target_timestamp = datetime.timestamp(now + timedelta(hours=10))
    if target_timestamp > exp_timestamp:
        # 기존 redis에 존재하는 token 삭제
        jwt_redis.delete(token)
        refresh_token = create_refresh_token(identity=user_id)
        set_refresh_cookies(response=response, encoded_refresh_token=refresh_token)
        # redis에 토큰 저장
        jwt_redis.set(refresh_token, user_id, ex=timedelta(days=14))

    return response