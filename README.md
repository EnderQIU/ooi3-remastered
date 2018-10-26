![Header](https://raw.githubusercontent.com/EnderQIU/ooi3-remastered/4.2.1.0/static/img/logo.png)
# OOI v3 Remastered
Online Objects Integration (OOI) system based on flask & requests.

## Features
1. Updated various of python packages.
2. Flask-caching static files with redis.
3. HTTPS Supported.
4. Running in 2nd Sequence (HTML5 game mode).
5. Embedded kancolle staff twitter off-canvas.

## Main Outlook
- [ ] Assistant tools embedded on the website page for cross-platform gaming.
- [ ] Automatic API version update.

## 4.2.1.0 Branch
**Important** It seems like that the previous API version will be banned after the official server
maintance except API version 4.0.0.0 as far as I can tell. So please use branch 4.0.0.0 if you are tired
of updating API version frequently. I'm considering adding API version choices in the next version
of the ooi3-remastered but that's not the point.


This branch use API version 4.2.1.0 and its default iframe plugin is html5 which is 
supported by all modern desktop and mobile devices. Since it's a new API version, I'm quite
not sure what would happen under it. Any issue or pull requests are welcomed.

## Demo Website
You can visit this [demo website](https://ooi.enderqiu.cn/) to preview all features (HTTPS supported).
We highly recommend you deploy this site on the VPS owned by yourself with HTTPS if you are worried
about some security problems.

## Dependency
- The memory is suggested to be higher than 512MB if you switch on the Redis-File-Cache.
- Ubuntu 16.04 with bbr. (Recommend, other OS is ok. BBR can perform a better upload traffic.)
- Nginx
- Supervisor
- uwsgi
- python 3.5 or higher

## Deploy
Please refer to the config files in the `deploy/` directory.

Following four environment variables should be set if use the tweets feature.

| KEY                | VALUE                                      |
| :----------------- | :----------------------------------------- |
| ACCESS_KEY         | Consumer API key for twitter developers    |
| SECRET_KEY         | Consumer API secret for twitter developers |
| ACCESS_TOKEN       | Access token for twitter developers        |
| TOKEN_SECRET       | Token secret for twitter developers        |

## Trouble Shooter
1. Q: Any *Permission Denied* error:

A: `chown -R www-data:www-data /srv/ooi3-remastered/`

2. Q: Got `local.Error: unsupported locale setting`:

A: `export LC_ALL=C`

3. Q: How to use proxy?

A: Set the environment variables: `HTTP_PROXY` or `HTTPS_PROXY` e.g. `export HTTP_PROXY="http://127.0.0.1:1087`.

4. Q: No data caught by POI when start in POI mode using HTTPS?

A: Don't forcefully redirect HTTP to HTTPS because POI can't catch HTTPS data.

5. Got 'Cannot get DMM token, are you in Japan?' while local debugging.

A: Set `FLASK_ENV` to `development` and check `Do not start game` on main page
   to debug HTML pages without login into the game.
   
6. Q: Got `SyntaxError: invalid syntax` when `import tweepy` from tweepy 3.6.0.

A: The tweepy 3.6.0 uses the keyword `async` in Python 3.7. You can use Python 3.6 or former. Or you can replace 
   all `async` variables in tweepy/streaming.py to _async or something else.
   
## Acknowledgement
Portion of this software may utilize the following copyrighted materials, the use of which is hereby acknowledged.

- [xterm.js](https://xtermjs.org) MIT License
- [acgx/ooi3](https://github.com/acgx/ooi3) GPLv3 License
- [ajax-hook](https://github.com/wendux/Ajax-hook)

## License
GPLv3 License
