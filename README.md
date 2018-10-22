# OOI v3 Remastered
Online Objects Integration (OOI) system based on flask & requests.

Updated various of python packages. Remastered cdn cache with qiniu.

# Use qiniu CDN

## Trouble Shooter
1. Q: Any *Permission Denied* error:

A: `chown -R www-data:www-data /srv/ooi3-remastered/`

2. Q: Got `local.Error: unsupported locale setting`:

A: `export LC_ALL=C`

3. Q: How to use proxy?

A: Use environment variables: `HTTP_PROXY` or `HTTPS_PROXY` such as `export HTTP_PROXY="http://127.0.0.1:1087`.

4. Q: How to use qiniu cdn?

A: Set the environment variables: `QINIU_ACCESS_KEY`, `QINIU_SECRET_KEY` and `QINIU_BUCKET_NAME` to yours.