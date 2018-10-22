from flask import Response


class BadResponse(Response):
    """
    错误响应类
    """
    def __init__(self):
        super().__init__()
        self.status=400


class JsonResponse(Response):
    """
    Json 响应类
    """
