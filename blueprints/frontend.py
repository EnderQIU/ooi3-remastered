"""OOI3的前端部分，用于显示各种页面。
包含了登录表单、登录后的跳转、不同的游戏运行模式和注销页面。
"""
from flask import redirect, Blueprint, session, request, url_for

from app import app
from auth.kancolle import KancolleAuth, OOIAuthException
from base.response import BadResponse, render_minify_template

frontend_bp = Blueprint('frontend', __name__)


@frontend_bp.route('/', methods=('GET',))
def form():
    """Display login form

    :return: rv
    """
    if 'mode' in session:
        mode = session['mode']
    else:
        session['mode'] = 1
        mode = 1
    return render_minify_template('form.html', mode=mode)


def debug_login(login_id, password, mode):
    """
    login page for local debug.
    :param login_id:
    :param password:
    :param mode:
    :return:
    """
    if login_id and password:
        if mode in (1, 2, 3):
            # kancolle_auth = KancolleAuth(login_id, password)
            try:
                # kancolle_auth.get_entry()
                session['api_token'] = 'api_token'
                session['api_starttime'] = 'api_starttime'
                session['world_ip'] = 'world_ip'
                if mode == 2:
                    return redirect('/kcv')
                elif mode == 3:
                    return redirect('/poi')
                else:
                    return redirect('/browser')
            except OOIAuthException as e:
                return render_minify_template('form.html', errmsg=e.message, mode=mode)
        elif mode == 4:
            try:
                # osapi_url = kancolle_auth.get_osapi()
                session['osapi_url'] = 'osapi_url'
                return redirect('/connector')
            except OOIAuthException as e:
                return render_minify_template('form.html', errmsg=e.message, mode=mode)
        else:
            return BadResponse("Invalid mode")
    else:
        return render_minify_template('form.html', errmsg='Please input your username and password.', mode=mode)


@frontend_bp.route('/', methods=('POST',))
def login():
    """Login DMM from login form

    :return: rv
    """
    post = request.form
    login_id = post.get('login_id', None)
    password = post.get('password', None)
    mode = int(post.get('mode', 1))

    # Test mode for local debug
    test_mode = post.get('testMode', False)
    if test_mode:
        test_mode = True
    session['test_mode'] = test_mode
    session['mode'] = mode

    if app.config['ENV'] == 'development' and test_mode:
        return debug_login(login_id, password, mode)

    if login_id and password:
        kancolle_auth = KancolleAuth(login_id, password)
        if mode in (1, 2, 3):
            try:
                kancolle_auth.get_entry()
                session['api_token'] = kancolle_auth.api_token
                session['api_starttime'] = kancolle_auth.api_starttime
                session['world_ip'] = kancolle_auth.world_ip
                if mode == 2:
                    return redirect('/kcv')
                elif mode == 3:
                    return redirect('/poi')
                else:
                    return redirect('/browser')
            except OOIAuthException as e:
                return render_minify_template('form.html', errmsg=e.message, mode=mode)
        elif mode == 4:
            try:
                osapi_url = kancolle_auth.get_osapi()
                session['osapi_url'] = osapi_url
                return redirect('/connector')
            except OOIAuthException as e:
                return render_minify_template('form.html', errmsg=e.message, mode=mode)
        else:
            return BadResponse("Invalid mode")
    else:
        return render_minify_template('form.html', errmsg='Please input your username and password.', mode=mode)


def debug_browser():
    """
    kancolle page for local debug
    :return:
    """
    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        context = {'scheme': request.scheme,
                   'host': request.host + '/js_mobile_console?realSrc=',
                   'token': token,
                   'starttime': starttime,
                   'local_debug': 'yes',
                   }
        return render_minify_template('browser.html', **context)
    else:
        session.clear()
        return redirect('/')


@frontend_bp.route('/js_mobile_console', methods=('GET',))
def debug_js_mobile_console():
    """
    Embedded page for local debug
    :return:
    """
    return render_minify_template("js_mobile_console.html")


@frontend_bp.route('/browser', methods=('GET',))
def browser():
    """适配浏览器中进行游戏的页面，该页面会检查会话中是否有api_token、api_starttime和world_ip三个参数，缺少其中任意一个都不能进行
    游戏，跳转回登录页面。

    :return: rv
    """
    if app.config['ENV'] == 'development' and session.get('test_mode', False):
        return debug_browser()

    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        context = {'scheme': request.scheme,
                   'host': request.host,
                   'token': token,
                   'starttime': starttime}
        return render_minify_template('browser.html', **context)
    else:
        session.clear()
        return redirect('/')


def debug_kcv():
    """
    kcv page for local debug
    :return:
    """
    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        return render_minify_template('kcv.html', context={})
    else:
        session.clear()
        return redirect('/')


@frontend_bp.route('/kcv', methods=('GET',))
def kcv():
    """适配KanColleViewer或者74EO中进行游戏的页面，提供一个iframe，在iframe中载入游戏FLASH。该页面会检查会话中是否有api_token、
    api_starttime和world_ip三个参数，缺少其中任意一个都不能进行游戏，跳转回登录页面。

    :return: rv
    """
    if app.config['ENV'] == 'development' and session.get('test_mode', False):
        return debug_kcv()

    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        return render_minify_template('kcv.html', context={})
    else:
        session.clear()
        return redirect('/')


def debug_flash():
    """
    flash page for local debug
    :return:
    """
    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        context = {'scheme': request.scheme,
                   'host': request.host + '/static/img/game.png?realSrc=',
                   'token': token,
                   'starttime': starttime}
        return render_minify_template('flash.html', **context)
    else:
        session.clear()
        return redirect('/')


@frontend_bp.route('/flash', methods=('GET',))
def flash():
    """适配KanColleViewer或者74EO中进行游戏的页面，展示，该页面会检查会话中是否有api_token、api_starttime和world_ip三个参数，
    缺少其中任意一个都不能进行游戏，跳转回登录页面。

    :return: rv
    """
    if app.config['ENV'] == 'development' and session.get('test_mode', False):
        return debug_flash()

    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        context = {'scheme': request.scheme,
                   'host': request.host,
                   'token': token,
                   'starttime': starttime}
        return render_minify_template('flash.html', **context)
    else:
        session.clear()
        return redirect('/')


def debug_poi():
    """
    poi page for local test
    :return:
    """
    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        context = {'scheme': request.scheme,
                   'host': request.host + '/static/img/game.png?realSrc=',
                   'token': token,
                   'starttime': starttime}
        return render_minify_template('poi.html', **context)
    else:
        session.clear()
        return redirect('/')


@frontend_bp.route('/poi', methods=('GET',))
def poi():
    """适配poi中进行游戏的页面，显示FLASH。该页面会检查会话中是否有api_token、api_starttime和world_ip三个参数，缺少其中任意一个
    都不能进行游戏，跳转回登录页面。

    :return: rv
    """
    if app.config['ENV'] == 'development' and session.get('test_mode', False):
        return debug_poi()

    # Use http for POI
    if request.scheme == 'https' and app.config['ENV'] == 'production':
        return redirect(url_for('frontend.poi', _scheme="http", _external=True))
    token = session.get('api_token', None)
    starttime = session.get('api_starttime', None)
    world_ip = session.get('world_ip', None)
    if token and starttime and world_ip:
        context = {'scheme': request.scheme,
                   'host': request.host,
                   'token': token,
                   'starttime': starttime}
        return render_minify_template('poi.html', **context)
    else:
        session.clear()
        return redirect('/')


def debug_connector():
    """
    connector page for local debug
    :return:
    """
    osapi_url = session.get('osapi_url', None)
    if osapi_url:
        context = {'osapi_url': osapi_url}
        return render_minify_template('connector.html', **context)
    else:
        session.clear()
        return redirect('/')


@frontend_bp.route('/connector', methods=('GET',))
def connector():
    """适配登录器直连模式结果页面，提供osapi.dmm.com的链接。

    :return: rv
    """
    if app.config['ENV'] == 'development' and session.get('test_mode', False):
        return debug_connector()

    osapi_url = session.get('osapi_url', None)
    if osapi_url:
        context = {'osapi_url': osapi_url}
        return render_minify_template('connector.html', **context)
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
