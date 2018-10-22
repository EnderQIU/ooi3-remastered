from urllib.parse import urlencode

import click
import datetime
import requests
from flask import Blueprint, request, Response
from requests import Timeout
from qiniu import Auth, put_data

from base import config

cdn_bp = Blueprint('cdn', __name__)

q = Auth(config.access_key, config.secret_key)
bucket_name = config.bucket_name


def upload_file(key, data, mime_type='application/octet-stream'):
    token = q.upload_token(bucket_name, key, 30)
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


@cdn_bp.route('/kcs2/<path:static_path>', methods=('GET',))
def kcs2(static_path):
    url = config.upstream + 'kcs2/' + static_path

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
        if len(request.args) > 0:
            upload_file('kcs2/' + static_path + '?' + urlencode(request.args),
                        resp.content,
                        resp.headers.get('Content-Type', 'application/octet-stream'))
        else:
            upload_file('kcs2/' + static_path,
                        resp.content,
                        resp.headers.get('Content-Type', 'application/octet-stream'))

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response
