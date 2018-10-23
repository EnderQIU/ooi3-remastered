import os

# Proxies
proxies = {
    'http': os.environ.get('HTTP_PROXY'),
    'https': os.environ.get('HTTPS_PROXY'),
}

# static files upstream server
upstream = 'http://203.104.209.102/'

# qiniu cdn
access_key = os.environ.get('QINIU_ACCESS_KEY')
secret_key = os.environ.get('QINIU_SECRET_KEY')
bucket_name = os.environ.get('QINIU_BUCKET_NAME')
cdn_hostname = os.environ.get('QINIU_CDN_HOSTNAME')  # must end with slash
