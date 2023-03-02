Unofficial Python Wrapper Library for CookieCloud
=======
[![Build Status](https://app.travis-ci.com/lupohan44/PyCookieCloud.svg?branch=master)](https://app.travis-ci.com/lupohan44/PyCookieCloud)

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/lupohan44)

`PyCookieCloud` is is an unofficial Python wrapper library for [CookieCloud](https://github.com/easychen/CookieCloud). The decryption of data happens on the client side.

Table of Content
================

* [Installation](#installation)

* [Usage](#usage)

* [License](#license)


Installation
============

```
pip install PyCookieCloud
```

**Windows user might need to rename your ```Python\PythonXX\Lib\site-packages\crypto``` to ```Python\PythonXX\Lib\site-packages\Crypto```**

Usage
=======
```python
from PyCookieCloud import PyCookieCloud


def main():
    cookie_cloud = PyCookieCloud('YOUR_COOKIE_CLOUD_URL', 'YOUR_COOKIE_CLOUD_UUID', 'YOUR_COOKIE_CLOUD_PASSWORD')
    the_key = cookie_cloud.get_the_key()
    if not the_key:
        print('Failed to get the key')
        return
    encrypted_data = cookie_cloud.get_encrypted_data()
    if not encrypted_data:
        print('Failed to get encrypted data')
        return
    decrypted_data = cookie_cloud.get_decrypted_data()
    if not decrypted_data:
        print('Failed to get decrypted data')
        return
    print(decrypted_data)
    another_cookie_cloud = PyCookieCloud('YOUR_COOKIE_CLOUD_URL', 'YOUR_COOKIE_CLOUD_UUID_2', 'YOUR_COOKIE_CLOUD_PASSWORD_2')
    if not another_cookie_cloud.update_cookie(decrypted_data):
        print('Failed to update cookie')
        return
    another_decrypted_data = another_cookie_cloud.get_decrypted_data()
    print(another_decrypted_data)
    print(decrypted_data == another_decrypted_data)


if __name__ == '__main__':
    main()

```

License
=======
[MIT](LICENSE)