"""OOI3的前端部分，用于显示各种页面。
包含了登录表单、登录后的跳转、不同的游戏运行模式和注销页面。
"""
from flask import render_template, redirect, Response, Blueprint, session, request

from auth.kancolle import KancolleAuth, OOIAuthException

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/', methods=('GET',))
def index():
    """Display login form

    :return: rv
    """
    if 'mode' in session:
        mode = session['mode']
    else:
        session['mode'] = 1
        mode = 1
    return render_template('form.html', mode=mode)


@frontend_bp.route('/', methods=('POST',))
def form():
    """Login DMM from login form

    :return: rv
    """
    post = request.form
    login_id = post.get('login_id', None)
    password = post.get('password', None)
    mode = int(post.get('mode', 1))
    session['mode'] = mode
    if login_id and password:
        kancolle = KancolleAuth(login_id, password)
        if mode in (1, 2, 3):
            try:
                kancolle.get_entry()
                session['api_token'] = kancolle.api_token
                session['api_starttime'] = kancolle.api_starttime
                session['world_ip'] = kancolle.world_ip
                if mode == 2:
                    return redirect('/kcv')
                elif mode == 3:
                    return redirect('/poi')
                else:
                    return redirect('/kancolle')
            except OOIAuthException as e:
                return render_template('form.html', errmsg=e.message, mode=mode)
        elif mode == 4:
            try:
                osapi_url = kancolle.get_osapi()
                session['osapi_url'] = osapi_url
                return redirect('/connector')
            except OOIAuthException as e:
                return render_template('form.html', errmsg=e.message, mode=mode)
        else:
            return Response(status=400)
    else:
        return render_template('form.html', errmsg='Please input your username and password.', mode=mode)


@frontend_bp.route('/normal', methods=('GET',))
def normal():
    """适配浏览器中进行游戏的页面，该页面会检查会话中是否有api_token、api_starttime和world_ip三个参数，缺少其中任意一个都不能进行
    游戏，跳转回登录页面。

    :return: rv
    """
    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        context = {'scheme': request.scheme,
                   'host': request.host,
                   'token': token,
                   'starttime': starttime}
        return render_template('normal.html', **context)
    else:
        session.clear()
        return redirect('/')


@frontend_bp.route('/kcv', methods=('GET',))
def kcv():
    """适配KanColleViewer或者74EO中进行游戏的页面，提供一个iframe，在iframe中载入游戏FLASH。该页面会检查会话中是否有api_token、
    api_starttime和world_ip三个参数，缺少其中任意一个都不能进行游戏，跳转回登录页面。

    :return: rv
    """
    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        return render_template('kcv.html', context={})
    else:
        session.clear()
        return redirect('/')


@frontend_bp.route('/flash', methods=('GET',))
def flash():
    """适配KanColleViewer或者74EO中进行游戏的页面，展示，该页面会检查会话中是否有api_token、api_starttime和world_ip三个参数，
    缺少其中任意一个都不能进行游戏，跳转回登录页面。

    :return: rv
    """
    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        context = {'scheme': request.scheme,
                   'host': request.host,
                   'token': token,
                   'starttime': starttime}
        return render_template('flash.html', **context)
    else:
        session.clear()
        return redirect('/')


@frontend_bp.route('/poi', methods=('GET',))
def poi():
    """适配poi中进行游戏的页面，显示FLASH。该页面会检查会话中是否有api_token、api_starttime和world_ip三个参数，缺少其中任意一个
    都不能进行游戏，跳转回登录页面。

    :return: rv
    """
    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        context = {'scheme': request.scheme,
                   'host': request.host,
                   'token': token,
                   'starttime': starttime}
        return render_template('poi.html', **context)
    else:
        session.clear()
        return redirect('/')


@frontend_bp.route('/connector', methods=('GET',))
def connector():
    """适配登录器直连模式结果页面，提供osapi.dmm.com的链接。

    :return: rv
    """
    osapi_url = session.get('osapi_url', None)
    if osapi_url:
        context = {'osapi_url': osapi_url}
        return render_template('connector.html', **context)
    else:
        session.clear()
        return redirect('/')


@frontend_bp.route('/logout', methods=('GET',))
def logout():
    """ 注销已登录的用户。
    清除所有的session，返回首页。

    :return: rv
    """
    session.clear()
    return redirect('/')
