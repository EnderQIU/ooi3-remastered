import datetime
from urllib.parse import urlencode, quote

import click
import requests
from flask import Blueprint, request, Response, jsonify
from qiniu import BucketManager, put_data
from requests import Timeout

from base import config
from base.response import redirect_with_allow_origin

cdn_bp = Blueprint('cdn', __name__)


def upload_file(key, data, mime_type='application/octet-stream'):
    """
    Upload files to qiniu cdn
    :param key:
    :param data:
    :param mime_type:
    :return:
    """
    from ooi import qiniu

    token = qiniu.upload_token(config.bucket_name, key, 30)
    ret, info = put_data(up_token=token,
                         key=key,
                         data=data,
                         mime_type=mime_type)
    if info.status_code == 200:
        from ooi import cached_file_names
        cached_file_names.append(key)
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
    from ooi import cached_file_names

    upstream_url = config.upstream + ver + static_path
    if len(request.args) > 0:
        full_path = ver + static_path + '?' + urlencode(request.args)
    else:
        full_path = ver + static_path
    # CDN redirect

    if full_path in cached_file_names:
        return redirect_with_allow_origin(config.cdn_hostname + quote(full_path))

    try:
        resp = requests.request(
            method=request.method,
            url=upstream_url,
            params=request.args,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False)
    except Timeout:
        return Response(status=504)

    if resp.ok:
        from ooi import q
        q.enqueue_call(func=upload_file,
                       args=(full_path,
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


def _cdn_list():
    from ooi import qiniu

    bucket = BucketManager(qiniu)
    prefix = None
    limit = None
    delimiter = None
    marker = None
    ret, eof, info = bucket.list(config.bucket_name, prefix, marker, limit, delimiter)
    return ret, eof, info


@cdn_bp.route('/cdn_list', methods=('GET',))
def cdn_list():
    """
    Fetch the list of files available on cdn
    :return:
    """
    ret, eof, info = _cdn_list()
    return jsonify({'total': len(ret.get('items')), 'list': ret.get('items')})
