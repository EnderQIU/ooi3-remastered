# OOI v3 Remastered
Online Objects Integration (OOI) system based on flask & requests.

## Features
1. Updated various of python packages.
2. Flask-caching static files with redis.
3. HTTPS Supported.
4. Running in 2nd Sequence (HTML5 game mode).

## 4.2.0.2 Branch
This branch use API version 4.2.0.2 and its default iframe plugin is html5 which is 
supported by all modern desktop and mobile devices. Since its a new API version, I'm quite
not sure what would happen under it. Any issue or pull requests are welcomed.

## Trouble Shooter
1. Q: Any *Permission Denied* error:

A: `chown -R www-data:www-data /srv/ooi3-remastered/`

2. Q: Got `local.Error: unsupported locale setting`:

A: `export LC_ALL=C`

3. Q: How to use proxy?

A: Use environment variables: `HTTP_PROXY` or `HTTPS_PROXY` such as `export HTTP_PROXY="http://127.0.0.1:1087`.