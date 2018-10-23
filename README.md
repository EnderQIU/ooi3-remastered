# OOI v3 Remastered
Online Objects Integration (OOI) system based on flask & requests.

Updated various of python packages. Remastered cdn cache with qiniu.

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