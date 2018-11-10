"""
Bundles **only** contains custom stylesheets and javascript.
Put those from vendor (jquery etc.) directly into the HTML.

Since static files produced by vendors won't change very frequently,
and minifying them using Flask-Assets can consume tons of CPU
times. We serve the static that belongs to this project by
Flask-Assets to version them for refreshing browser cache when
a new version is released. And Flask-Assets can minify them for
saving data traffic besides improving loading time of the site.
"""
from flask_assets import Bundle

bundles = {
    # base.html
    'base_js': Bundle(
        'js/base/ooi-base.js',
        output='dist/base.js',
        filters='jsmin',
    ),
    'base_css': Bundle(
        'css/base/ooi-base.css',
        output='dist/base.css',
        filters='cssmin',
    ),
    # form.html
    'form_js': Bundle(
        'js/form/ooi-tweets.js',
        output='dist/form.js',
        filters='jsmin',
    ),
    # browser.html
    # In this bundle you must be careful following the order below
    # to ensure the dependency graph is correct.
    'browser_js': Bundle(
        # bridge: The bridges between the game and the assistant.
        'js/browser/bridge/ooi-fullscreen.js',
        'js/browser/bridge/ooi-xhrhook.js',
        # service: For services used by plugins. Providing sealed data and data update listeners.
        # system: System-level plugins which have accessories to modify requests and responses.
        # plugins: For plugins only with accessories to get requests and responses.
        # views: GUI platform of assistant. Per-plugin's views should be put in their own directories.
        # main: The assistant entry point.
        'js/browser/main.js',
        output='dist/browser.js',
        filters='jsmin',
    ),
    'browser_css': Bundle(
        'css/browser/ooi-browser.css',
        output='dist/browser.css',
        filters='cssmin',
    ),
    # poi.html
    'poi_js': Bundle(
        'js/poi/ooi-poi.js',
        output='dist/poi.js',
        filters='jsmin',
    ),
    'poi_css': Bundle(
        'css/poi/ooi-poi.css',
        output='dist/poi.css',
        filters='cssmin',
    ),
    # ios.html
    'ios_js': Bundle(
        'js/ios/ooi-iosjsbridge.js',
        'js/ios/ooi-iosfullscreen.js',
        'js/ios/main.js',
        output='dist/ios.js',
        filters='jsmin',
    ),
    'ios_css': Bundle(
        'css/ios/ooi-ios.css',
        output='dist/ios.css',
        filters='cssmin',
    ),
}
