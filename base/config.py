import os

# Proxies
proxies = {
    'http': os.environ.get('HTTP_PROXY'),
    'https': os.environ.get('HTTPS_PROXY'),
}

# static files upstream server
upstream = 'http://203.104.209.102/'

assert upstream.endswith('/'), 'config.upstream must ends with slash.'
