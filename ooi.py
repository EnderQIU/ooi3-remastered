"""OOI3: Online Objects Integration version 3.0"""

import argparse
import os

import click
from flask import Flask
from qiniu import Auth

from base import config
from blueprints.api import api_bp
from blueprints.cdn import cdn_bp, fetch_cdn_list
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

# Shared vars
qiniu = Auth(config.access_key, config.secret_key)

# qiniu init
bucket_name = config.bucket_name

# Fetch cdn cached file list
items = fetch_cdn_list()
cached_file_names = [i.get('key') for i in items]
if cached_file_names is None:  # init repo is None
    cached_file_names = []

app = Flask(__name__)

app.config['SECRET_KEY'] = os.urandom(24)

app.register_blueprint(api_bp)
app.register_blueprint(frontend_bp)
app.register_blueprint(service_bp)
app.register_blueprint(cdn_bp)


def detect_proxies():
    proxies = config.proxies
    if proxies.get('http') is not None:
        click.echo(' * HTTP proxy detected: {0}'.format(proxies.get('http')))
    if proxies.get('https') is not None:
        click.echo(' * HTTPS proxy detected: {0}'.format(proxies.get('https')))
    if proxies.get('http') is None and proxies.get('https') is None:
        click.echo(' * No HTTP proxy detected, make sure your server\'s ip is in Japan.')


def check_env():
    """
    Check all environment variables are set correctly
    :return:
    """
    if config.access_key is None \
            or config.secret_key is None \
            or config.bucket_name is None:
        click.echo('Please set all environment variables correctly!')
        exit(1)


if __name__ == '__main__':
    detect_proxies()
    check_env()

    app.run(host=host, port=port, debug=debug)
