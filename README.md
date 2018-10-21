# OOI v3 Remastered
Online Objects Integration (OOI) system based on aiohttp.

Updated various of python packages. Remastered cdn cache method.

This system requires the Python version >=3.5.3 for using the newest aiohttp in order to achieve the best efficiency。

## Trouble Shooter
1. Q: Got shucked when executing `pip install -r requirements.txt` on macOS?

A: Add `--global-option=build_ext --global-option="-L/usr/local/opt/openssl/lib" --global-option="-I/usr/local/opt/openssl/include"` to
`pip install -r requirements.txt`  to help find openssl header files.

2. Q: Got `ValueError: Fernet key must be 32 url-safe base64-encoded bytes.`

A: Add environment variable `OOI_SECRET_KEY` with the value of 32 url-safe base64-encoded bytes.

3. Q: Any *Permission Denied* error:

A: `chown -R www-data:www-data /srv/ooi3-remastered/`

4. Q: Got `local.Error: unsupported locale setting`:

A: `export LC_ALL=C`

5. Q: How to use proxy?

A: Use environment variables: `HTTP_PROXY` or `HTTPS_PROXY` such as `export HTTP_PROXY="http://127.0.0.1:1087`.