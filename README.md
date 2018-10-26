# OOI v3 Remastered
Online Objects Integration (OOI) system based on flask & requests.

## Features
1. Updated various of python packages.
2. Flask-caching static files with redis.

## API version
**Important:** It seems like that the previous API version will be banned after the official server maintance except API version 4.0.0.0 as far as I can tell. So please use branch 4.0.0.0 if you are tired of updating API version frequently. I'm considering adding API version choices in the next version of the ooi3-remastered but that's not the point.


This branch use API version 4.0.0.0 and the default embed plugin is Flash Player
 which not support iOS devices. It will **not be updated** in the future but it
 is convinient for those who just looks for the stable service. So I decided to 
 keep this branch.
If you are looking for new features, Please checkout the newest branch for a better experience.

## Trouble Shooter
1. Q: Any *Permission Denied* error:

A: `chown -R www-data:www-data /srv/ooi3-remastered/`

2. Q: Got `local.Error: unsupported locale setting`:

A: `export LC_ALL=C`

3. Q: How to use proxy?

A: Use environment variables: `HTTP_PROXY` or `HTTPS_PROXY` such as `export HTTP_PROXY="http://127.0.0.1:1087`.

4. Q: Why I got a CORS exception on Chrome?

A: That maybe a chrome bug, install the CORS plugin for chrome will fix that.

5. Q: Async version available?

A: Of course yes. Checkout git reflog #462e148. If your VPS's memeory is under or equal 512MB, I recommend you not to
   use it.
