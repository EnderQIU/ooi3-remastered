from urllib.parse import urlencode

import requests
from flask import Blueprint, request, Response
from requests import Timeout

from base import config

cdn_bp = Blueprint('cdn', __name__)


def _kcs(ver, static_path):
    """
    Handel static files
    :param ver:
    :param static_path:
    :return:
    """
    url = config.upstream + ver + static_path

    try:
        resp = requests.request(
            method=request.method,
            url=url,
            params=request.args,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False)
    except Timeout:
        return Response(status=504)

    if resp.ok:
        from ooi import q, upload_file
        if len(request.args) > 0:
            q.enqueue_call(func=upload_file,
                           args=(ver + static_path,
                                 resp.content,
                                 resp.headers.get('Content-Type', 'application/octet-stream'),
                                 ),
                           result_ttl=10
                           )
        else:
            q.enqueue_call(func=upload_file,
                           args=(ver + static_path + '?' + urlencode(request.args),
                                 resp.content,
                                 resp.headers.get('Content-Type', 'application/octet-stream'),
                                 ),
                           result_ttl=10
                           )

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response


@cdn_bp.route('/kcs2/<path:static_path>', methods=('GET',))
def kcs2(static_path):
    return _kcs('kcs2/', static_path)


@cdn_bp.route('/kcs/<path:static_path>', methods=('GET',))
def kcs(static_path):
    return _kcs('kcs/', static_path)
