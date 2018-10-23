import datetime
from urllib.parse import urlencode, quote

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

    if len(request.args) > 0:
        path = ver + static_path + '?' + urlencode(request.args)
    else:
        path = ver + static_path

    # CDN redirect
    if path in cached_file_names:  # CDN hit
        click.echo("[{time}] CDN hit for {path}".format(time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                        path=path))
        full_path = config.cdn_hostname + quote(path)  # urlencode is needed for qiniu
    else:
        full_path = config.upstream + path

    try:
        resp = requests.request(
            method=request.method,
            url=full_path,
            params=request.args,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False)
    except Timeout:
        return Response(status=504)

    if resp.ok and not path.startswith('kcs2/index.php'):   # IMPORTANT!! cache this file will expose your token
                                                            # and cause CORS error!
        upload_file(full_path, resp.content, resp.headers.get('Content-Type', 'application/octet-stream'))

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]
    if 'index.php' in full_path:
        headers.append(('Access-Control-Allow-Origin', '*'))  # Enable CORS for index.php

    response = Response(resp.content, resp.status_code, headers)
    return response


@cdn_bp.route('/kcs2/<path:static_path>', methods=('GET',))
def kcs2(static_path):
    return _kcs('kcs2/', static_path)


@cdn_bp.route('/kcs/<path:static_path>', methods=('GET',))
def kcs(static_path):
    return _kcs('kcs/', static_path)


def fetch_cdn_list():
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
    ret, eof, info = fetch_cdn_list()
    return jsonify({'total': len(ret.get('items')), 'list': ret.get('items')})
