class CustomException(Exception):
    status_code = 601
    message = '요청 실패'

    def __init__(self):
        super().__init__()

    def to_json(self):
        response = dict(status=self.status_code, message=self.message)
        return response
