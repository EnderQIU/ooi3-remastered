import requests
from flask import Blueprint, request, Response
from requests import Timeout

from base import config

cdn_bp = Blueprint('cdn', __name__)


@cdn_bp.route('/kcs2/<path:static_path>', methods=('GET',))
def kcs2(static_path):
    url = config.upstream + 'kcs2/' + static_path

    method = request.method
    data = request.data or request.form or None
    headers = dict()
    for name, value in request.headers:
        if not value or name == 'Cache-Control':
            continue
        headers[name] = value

    try:
        r = requests.request(url=url,
                             method=method,
                             params=request.args,
                             headers=headers,
                             data=data,
                             stream=True,
                             proxies={'http:': config.upstream},
                             timeout=5)
    except Timeout:
        return Response(status=403)
    resp_headers = []
    for name, value in r.headers.items():
        if name.lower() in ('content-length', 'connection',
                            'content-encoding'):
            continue
        resp_headers.append((name, value))
    return Response(r.text, status=r.status_code, headers=resp_headers)
