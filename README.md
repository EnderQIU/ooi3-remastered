# OOI v3 Remastered
Online Objects Integration (OOI) system based on aiohttp.

Updated various of python packages. Remastered cdn cache method.

本系统要求Python版本**必须**大于等于3.5.3，利用最新的aiohttp库()来实现OOI系统，以期望获得更高的效率。

本系统在 kancolle.py 中进行登录时换用 requests 库，在进行登录时并发效率较低。

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