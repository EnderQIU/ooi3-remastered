"""OOI3: Online Objects Integration version 3.0 Remastered"""

import os
import configparser

from flask import Flask
from flask_assets import Environment
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

app.config['SECRET_KEY'] = os.urandom(24)

config = configparser.ConfigParser()
if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'config.ini')):
    print('"config.ini" not found. Please get one from "config.example.ini".')
    exit(1)
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

# Twitter Developers API
app.config['TWITTER_API_KEY'] = config.get('tweets-optional', 'TWITTER_API_KEY', fallback=None)
app.config['TWITTER_SECRET_KEY'] = config.get('tweets-optional', 'TWITTER_SECRET_KEY', fallback=None)
app.config['TWITTER_ACCESS_TOKEN'] = config.get('tweets-optional', 'TWITTER_ACCESS_TOKEN', fallback=None)
app.config['TWITTER_TOKEN_SECRET'] = config.get('tweets-optional', 'TWITTER_TOKEN_SECRET', fallback=None)


# Minify HTML
app.config['ENABLE_MINIFY'] = config.getboolean('debug-optional', 'ENABLE_MINIFY', fallback=False)

# Web Assets Debug
# If set to True, js and css will be loaded separated, else them will be spliced to one file in order
app.config['ASSETS_DEBUG'] = config.getboolean('debug-optional', 'ASSETS_DEBUG', fallback=False)

# API version
app.config['API_VERSION'] = config.get('required', 'API_VERSION', fallback='4.0.0.0')


def register_blueprints():
    from blueprints.api import api_bp
    from blueprints.cdn import cdn_bp
    from blueprints.frontend import frontend_bp
    from blueprints.service import service_bp
    from blueprints.ooiapi import ooiapi_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(frontend_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(cdn_bp)
    app.register_blueprint(ooiapi_bp)


def register_assets_bundles():
    from util.assets import bundles
    assets = Environment(app)
    assets.register(bundles)


register_blueprints()
register_assets_bundles()
