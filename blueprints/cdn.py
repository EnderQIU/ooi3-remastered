import datetime
from urllib.parse import urlencode

import click
import requests
from flask import Blueprint, request, Response, jsonify
from qiniu import BucketManager, put_data
from requests import Timeout

from base import config

cdn_bp = Blueprint('cdn', __name__)


def upload_file(key, data, mime_type='application/octet-stream'):
    """
    Upload files to qiniu cdn
    :param key:
    :param data:
    :param mime_type:
    :return:
    """
    token = qiniu.upload_token(config.bucket_name, key, 30)
    ret, info = put_data(up_token=token,
                         key=key,
                         data=data,
                         mime_type=mime_type)
    if info.status_code == 200:
        click.echo("[{time}] Upload success for {key}".format(
            time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            key=key))
    else:
        click.echo("[{time}] Failed to upload {key}".format(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                            key=key))


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
        from ooi import q
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


@cdn_bp.route('/cdn_list', methods=('GET', ))
def cdn_list():
    """
    Fetch the list of files available on cdn
    :return:
    """
    from ooi import qiniu

    bucket = BucketManager(qiniu)
    prefix = None
    limit = None
    delimiter = None
    marker = None
    ret, eof, info = bucket.list(config.bucket_name, prefix, marker, limit, delimiter)

    return jsonify({'total': len(ret.get('items')), 'list': ret.get('items')})
