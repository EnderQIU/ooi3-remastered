# OOI v3 Remastered
Online Objects Integration (OOI) system based on aiohttp.

Updated various of python packages. Remastered cdn cache method.

本系统要求Python版本大于等于3.4，利用最新的aiohttp库()来实现OOI系统，以期望获得更高的效率。

另外请注意本项目采用了AGPLv3开源协议，和之前的ooi2项目的GPLv2不同。

## Trouble Shooter
1. pip install on macOS
Add `--global-option=build_ext --global-option="-L/usr/local/opt/openssl/lib" --global-option="-I/usr/local/opt/openssl/include"` to
`pip install -r requirements.txt`  to help find openssl header files.

