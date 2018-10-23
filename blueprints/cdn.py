from urllib.parse import urlencode

from flask import Blueprint, request

from base.response import CachedStaticResponse, NonCachedStaticResponse

cdn_bp = Blueprint('cdn', __name__)


def _kcs(ver, static_path):
    """
    Handel static files
    :param ver: kcs/ or kcs2/
    :param static_path:
    :return:
    """
    assert ver in ['kcs/', 'kcs2/'], '{time} Static path must start with kcs/ or kcs2/'

    # Build the complete key e.g. 'kcs2/css/main.css?version=1.0.0'
    if len(request.args) > 0:
        key = ver + static_path + '?' + urlencode(request.args)
    else:
        key = ver + static_path

    if key.startswith('kcs2/index.php'):
        return NonCachedStaticResponse(key, request)

    return CachedStaticResponse(key)


@cdn_bp.route('/kcs2/<path:static_path>', methods=('GET',))
def kcs2(static_path):
    return _kcs('kcs2/', static_path)


@cdn_bp.route('/kcs/<path:static_path>', methods=('GET',))
def kcs(static_path):
    return _kcs('kcs/', static_path)
