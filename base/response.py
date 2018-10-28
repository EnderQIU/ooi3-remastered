import datetime
import json

import click
import requests
from flask import Response, render_template
from requests import Timeout
from htmlmin.main import minify

from base import config
from app import cache, app


class BadResponse(Response):
    """
    错误响应类
    """
    def __init__(self, message):
        super().__init__()
        time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        click.echo("[{time}] Bad Response: {msg}".format(time=time_str, msg=message))
        self.status_code = 400
        self.data = message


class JsonResponse(Response):
    """
    Json 响应类
    """
    def __init__(self, json_obj, **kwargs):
        super().__init__(**kwargs)
        self.data = json.dumps(json_obj)
        self.mimetype = 'text/json'


@cache.memoize(259200)
def get_cached_static_file(key):
    try:
        resp = requests.get(
            url=config.upstream + key,
            allow_redirects=False)
    except Timeout:
        return Response(status=504)

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    return resp.content, resp.status_code, headers


class CachedStaticResponse(Response):
    """
    Cached Static Files (e.g. /kcs2/css/main.css?version=1.0.0) response
    """
    def __init__(self, key):
        super().__init__()
        assert isinstance(key, str) and not key.startswith('/')

        cont, stat, header = get_cached_static_file(key)
        self.data = cont
        self.status_code = stat
        self.headers = header


class NonCachedStaticResponse(Response):
    """
    Non-cache Static Files (e.g. index.php) response
    """
    def __init__(self, key, request):
        super().__init__()
        assert isinstance(key, str) and key.startswith('kcs2/index.php')
        try:
            resp = requests.get(
                url=config.upstream + key,
                params=request.args,
                headers={key: value for (key, value) in request.headers if key != 'Host'},
                data=request.get_data(),
                cookies=request.cookies,
                allow_redirects=False)
        except Timeout:
            self.status_code = 504
            return

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

        self.data = resp.content
        self.status_code = resp.status_code
        self.headers = headers


def render_minify_template(template_name_or_list, **context):
    """
    Use this method will minify the templates when 'ENV' is set 'to production'
     or the 'enable_minify' parameter is set to True
    :param template_name_or_list:
    :param enable_minify: whether to minify the rendered templates
    :param context:
    :return:
    """
    if app.config['ENABLE_MINIFY'] or app.config['ENV'] == 'production':
        return minify(render_template(template_name_or_list, **context))
    else:
        return render_template(template_name_or_list, **context)
