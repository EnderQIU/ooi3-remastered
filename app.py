"""OOI3: Online Objects Integration version 3.0"""

import os

from flask import Flask
from flask_caching import Cache

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'redis'})

app.config['SECRET_KEY'] = os.urandom(24)

# Twitter API
app.config['API_KEY'] = os.environ.get('API_KEY', None)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', None)
app.config['ACCESS_TOKEN'] = os.environ.get('ACCESS_TOKEN', None)
app.config['TOKEN_SECRET'] = os.environ.get('TOKEN_SECRET', None)


def register_blueprints():
    from blueprints.api import api_bp
    from blueprints.cdn import cdn_bp
    from blueprints.frontend import frontend_bp
    from blueprints.service import service_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(frontend_bp)
    app.register_blueprint(service_bp)
    app.register_blueprint(cdn_bp)


register_blueprints()
