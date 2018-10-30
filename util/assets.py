"""
Bundles **only** contains custom stylesheets and javascript.
Put those from vendor (jquery etc.) directly into the HTML.
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
    'browser_js': Bundle(
        'js/browser/ooi-xhrhook.js',
        'js/browser/ooi-fullscreen.js',
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
}
