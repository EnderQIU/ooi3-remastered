"""OOI3: Online Objects Integration version 3.0"""

import argparse
import datetime
import os

import click
from flask import Flask
from qiniu import Auth, put_data
from rq import Queue
from worker import conn

from base import config
from blueprints.api import api_bp
from blueprints.cdn import cdn_bp
from blueprints.frontend import frontend_bp
from blueprints.service import service_bp

parser = argparse.ArgumentParser(description='Online Objects Integration version 3.0 Remastered')
parser.add_argument('-H', '--host', default='127.0.0.1',
                    help='The host of OOI server')
parser.add_argument('-p', '--port', type=int, default=5000,
                    help='The port of OOI server')
parser.add_argument('-D', '--debug', type=bool, default=False,
                    help='Enable Debug Mode of OOI Server')

# parse cli args
args = parser.parse_args()
host = args.host
port = args.port
debug = args.debug

# qiniu init
qiniu = Auth(config.access_key, config.secret_key)
bucket_name = config.bucket_name


def upload_file(key, data, mime_type='application/octet-stream'):
    token = qiniu.upload_token(bucket_name, key, 30)
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


app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

app.register_blueprint(api_bp)
app.register_blueprint(frontend_bp)
app.register_blueprint(service_bp)
app.register_blueprint(cdn_bp)

q = Queue(connection=conn)


def detect_proxies():
    proxies = config.proxies
    if proxies.get('http') is not None:
        click.echo(' * HTTP proxy detected: {0}'.format(proxies.get('http')))
    if proxies.get('https') is not None:
        click.echo(' * HTTPS proxy detected: {0}'.format(proxies.get('https')))
    if proxies.get('http') is None and proxies.get('https') is None:
        click.echo(' * No HTTP proxy detected, make sure your server\'s ip is in Japan.')


if __name__ == '__main__':
    detect_proxies()
    app.run(host=host, port=port, debug=debug)
