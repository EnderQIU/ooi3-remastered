"""OOI3的API服务。
只接受POST请求，包括login_id和password两个参数，返回用户的内嵌游戏网页地址或游戏FLASH地址。请求缺少参数时返回400错误。
"""

from flask import Response, Blueprint, request

from auth.exceptions import OOIAuthException
from auth.kancolle import KancolleAuth

service_bp = Blueprint('service', __name__)


@service_bp.route('/service/osapi', methods=('POST', ))
def get_osapi():
    """获取用户的内嵌游戏网页地址，返回一个JSON格式的字典。
    结果中`status`键值为1时获取成功，`osapi_url`键值为内嵌网页地址；`status`为0时获取失败，`message`键值提供了错误信息。

    :return: flask.Response
    """
    data = request.form
    login_id = data.get('login_id', None)
    password = data.get('password', None)
    if login_id and password:
        headers = {'Content-Type': 'application/json'}
        kancolle = KancolleAuth(login_id, password)
        try:
            osapi_url = kancolle.get_osapi()
            result = {'status': 1,
                      'osapi_url': osapi_url}
        except OOIAuthException as e:
            result = {'status': 0,
                      'message': e.message}
        return Response(result, headers=headers)
    else:
        return Response(status=400)


@service_bp.route('/service/flash', methods=('POST', ))
def get_flash():
    """获取用户的游戏FLASH地址，返回一个JSON格式的字典。
    结果中`status`键值为1时获取成功，`flash_url`键值为游戏FLASH地址；`status`为0时获取失败，`message`键值提供了错误信息。

    :return: flask.Response
    """
    data = request.form
    login_id = data.get('login_id', None)
    password = data.get('password', None)
    if login_id and password:
        headers = {'Content-Type': 'application/json'}
        kancolle = KancolleAuth(login_id, password)
        try:
            entry_url = kancolle.get_entry()
            result = {'status': 1,
                      'flash_url': entry_url}
        except OOIAuthException as e:
            result = {'status': 0,
                      'message': e.message}
        return Response(result, headers=headers)
    else:
        return Response(status=400)
