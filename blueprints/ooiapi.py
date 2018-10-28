from flask import Blueprint

from base.response import JsonResponse
from base.twitter import TwitterAPI

ooiapi_bp = Blueprint('ooiapi', __name__)


@ooiapi_bp.route('/ooiapi/twitter', methods=('GET', ))
def twitter():
    """
    Get most preview 20 tweets from Kancolle Staff's twitter
    :return:
    """
    twitter_api = TwitterAPI()
    return JsonResponse(twitter_api.get_official_20tweets())
