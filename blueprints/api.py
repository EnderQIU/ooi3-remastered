"""转发客户端FLASH和游戏服务器之间的通信。
接受客户端FLASH发送到OOI3服务器的请求，将其转发给用户所在的游戏服务器，获得响应后再返回给客户端FLASH。
"""

import requests
from flask import Response, Blueprint, session, request

from base import config

api_start2 = None
worlds = {}

api_bp = Blueprint('api', __name__)


@api_bp.route('/kcs/resources/image/world/{string:server}_{string:size}.png', methods=('GET', ))
def world_image(server, size):
    """ 显示正确的镇守府图片。
    舰娘游戏中客户端FLASH请求的镇守府图片是根据FLASH本身的URL生成的，需要根据用户所在的镇守府IP为其显示正确的图片。

    :return: aiohttp.web.HTTPFound or aiohttp.web.HTTPBadRequest
    """

    s = requests.Session()
    s.proxies = config.proxies
    s.timeout = 5

    world_ip = session['world_ip']
    if world_ip:
        ip_sections = map(int, world_ip.split('.'))
        image_name = '_'.join([format(x, '03') for x in ip_sections]) + '_' + size
        if image_name in worlds:
            body = worlds[image_name]
        else:
            url = 'http://203.104.209.102/kcs/resources/image/world/' + image_name + '.png'
            try:
                response = s.get(url=url)
            except requests.exceptions.Timeout:
                return Response(status=400)
            body = response.content
            worlds[image_name] = body
        return Response(body, headers={'Content-Type': 'image/png', 'Cache-Control': 'no-cache'})
    else:
        return Response(status=400)


@api_bp.route('/kcsapi/<string:action>', methods=('GET', 'POST', ))
def kcsapi(action):
    """ 转发客户端和游戏服务器之间的API通信。

    :param request: aiohttp.web.Request
    :return: aiohttp.web.Response or aiohttp.web.HTTPBadRequest
    """
    s = requests.Session()
    s.proxies = config.proxies
    s.timeout = 5

    world_ip = session.get('world_ip')
    if world_ip:
        if action == 'api_start2' and api_start2 is not None:
            return Response(api_start2,
                            headers={'Content-Type': 'text/plain'})
        else:
            referrer = request.headers.get('REFERER')
            referrer = referrer.replace(request.host, world_ip)
            referrer = referrer.replace('https://', 'http://')
            url = 'http://' + world_ip + '/kcsapi/' + action
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
                'Origin': 'http://' + world_ip + '/',
                'Referer': referrer,
            }
            data = request.post
            try:
                response = s.post(url=url, data=data, headers=headers)
            except requests.exceptions.Timeout:
                return Response(status=400)
            body = response.content
            if action == 'api_start2' and len(response.content) > 100000:
                api_start2 = body
            return Response(body, headers={'Content-Type': 'text/plain'})
    else:
        return Response(status=400)
