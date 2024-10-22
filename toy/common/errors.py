from .exceptions import *


def error_handle(api):
    """에러 핸들러

    에러 처리하는 함수

    Args:
        app  : __init__.py에서 파라미터로 app을 전달 받은 값
    Returns:
        json : error_response() 함수로 에러 메시지를 전달해서 반환 받고 return
    """
    @api.errorhandler(CustomException)
    def example_error(e: CustomException):
        return e.to_json(), e.to_json()['status']
        # response = e.to_json()  # 딕셔너리 형태로 반환된다고 가정
        # status_code = response.get('status', 500)  # 'status'가 없을 경우 기본 값으로 500 사용
        # return response, status_code
