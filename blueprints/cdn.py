from contextlib import closing

import requests
from flask import Blueprint, request, Response

from base import config

cdn_bp = Blueprint('cdn', __name__)


@cdn_bp.route('/kcs2/<path:static_path>', methods=('GET',))
def kcs2(static_path):
    url = config.upstream + 'kcs2/' + static_path + '?' + request.query_string
    method = request.method
    data = request.data or request.form or None
    headers = dict()
    for name, value in request.headers:
        if not value or name == 'Cache-Control':
            continue
        headers[name] = value

    with closing(
            requests.request(method, url, headers=headers, data=data, stream=True)
    ) as r:
        resp_headers = []
        for name, value in r.headers.items():
            if name.lower() in ('content-length', 'connection',
                                'content-encoding'):
                continue
            resp_headers.append((name, value))
        return Response(r, status=r.status_code, headers=resp_headers)
