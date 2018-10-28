from flask_assets import Bundle

bundles = {
    # base.html
    'base_js': Bundle(
        'js/vendor/jquery/jquery-3.3.1.js',
        'js/vendor/uikit/uikit.js',
        'js/ooi-base.js',
        output='dist/base.js',
        filters='jsmin',
    ),
    'base_css': Bundle(
        'css/vendor/uikit/uikit.css',
        'css/vendor/uikit/uikit.almost-flat.css',
        'css/ooi-base.css',
        output='dist/base.css',
        filters='cssmin',
    ),
    # form.html
    'form_js': Bundle(
        'js/ooi-tweets.js',
        output='dist/form.js',
        filters='jsmin',
    ),
    # browser.html
    'browser_js': Bundle(
        'js/vendor/ajaxhook/ajaxhook.min.js',
        'js/vendor/xterm/xterm.js',
        'js/ooi-xhrhook.js',
        'js/ooi-fullscreen.js',
        output='dist/browser.js',
        filters='jsmin',
    ),
    'browser_css': Bundle(
        'css/vendor/xterm/xterm.css',
        output='dist/browser.css',
        filters='cssmin',
    ),
    # poi.html
    'poi_js': Bundle(
        'js/ooi-poi.js',
        output='dist/poi.js',
        filters='jsmin',
    ),
    'poi_css': Bundle(
        'css/ooi-poi.css',
        output='dist/poi.css',
        filters='cssmin',
    ),
}
