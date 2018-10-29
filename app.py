"""OOI3: Online Objects Integration version 3.0 Remastered"""

import os

from flask import Flask
from flask_assets import Environment
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

app.config['SECRET_KEY'] = os.urandom(24)

# Twitter Developers API
app.config['API_KEY'] = os.environ.get('API_KEY', None)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)
app.config['ACCESS_TOKEN'] = os.environ.get('ACCESS_TOKEN', None)
app.config['TOKEN_SECRET'] = os.environ.get('TOKEN_SECRET', None)


# Minify HTML
app.config['ENABLE_MINIFY'] = os.environ.get('ENABLE_MINIFY', False)
if app.config['ENABLE_MINIFY'] == 'yes':
    app.config['ENABLE_MINIFY'] = True
else:
    app.config['ENABLE_MINIFY'] = False

# Web Assets Debug
app.config['ASSETS_DEBUG'] = os.environ.get('ASSETS_DEBUG', False)
if app.config['ASSETS_DEBUG'] == 'yes' or app.config['ENV'] == 'development':
    app.config['ASSETS_DEBUG'] = True
else:
    app.config['ASSETS_DEBUG'] = False

# API version
app.config['API_VERSION'] = os.environ.get('API_VERSION')


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
