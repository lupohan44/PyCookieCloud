import collections
import hashlib
import json
from typing import Optional, Dict, List, Any
from urllib.parse import urljoin,urlparse
from pathlib import Path

import requests

from .PyCryptoJS import encrypt, decrypt


class PyCookieCloud:
    def __init__(self, url: str, uuid: str, password: str):
        self.url: str = url
        self.uuid: str = uuid
        self.password: str = password
        self.api_root: str = urlparse(url).path if urlparse(url).path else None

    def check_connection(self) -> bool:
        """
        Test the connection to the CookieCloud server.

        :return: True if the connection is successful, False otherwise.
        """
        try:
            resp = requests.get(self.url)
            if resp.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            return False

    def get_encrypted_data(self) -> Optional[str]:
        """
        Get the encrypted data from the CookieCloud server.

        :return: The encrypted data if the connection is successful, None otherwise.
        """
        if self.check_connection():
            path = str(Path(self.api_root, 'get/', self.uuid))
            cookie_cloud_request = requests.get(urljoin(self.url, path))
            if cookie_cloud_request.status_code == 200:
                cookie_cloud_response = cookie_cloud_request.json()
                encrypted_data = cookie_cloud_response["encrypted"]
                return encrypted_data
            else:
                return None
        else:
            return None

    def get_decrypted_data(self) -> Optional[Dict[str, Any]]:
        """
        Get the decrypted data from the CookieCloud server.

        :return: decrypted data if the decryption is successful, None otherwise.
        """
        encrypted_data = self.get_encrypted_data()
        if encrypted_data is not None:
            try:
                decrypted_data = decrypt(encrypted_data, self.get_the_key().encode('utf-8')).decode('utf-8')
                decrypted_data = json.loads(decrypted_data)
                if 'cookie_data' in decrypted_data:
                    return decrypted_data['cookie_data']
            except Exception as e:
                return None
        else:
            return None

    def get_cookie_value(self, hostname: str, key: str) -> Optional[str]:
        """
        Get the cookie value from the CookieCloud server.

        :param hostname: the hostname of the cookie.
        :param key: the key of the cookie.
        :return: the cookie value if the decryption is successful, None otherwise.
        """
        decrypted_data = self.get_decrypted_data()
        if decrypted_data is not None:
            if hostname in decrypted_data:
                for value in decrypted_data[hostname]:
                    if value['name'] == key:
                        if 'value' in value:
                            return value['value']
        return None

    def get_cookie_str(self, hostname: str, keys: Optional[List[str]] = None, all_keys_required: bool = True) -> Optional[str]:
        """
        Get the cookie string from the CookieCloud server.

        :param hostname: the hostname of the cookie.
        :param keys: the keys of the cookie.
        :param all_keys_required: will return None if not all keys are matched when all_keys_required is True.
        :return:
        """
        decrypted_data = self.get_decrypted_data()
        if decrypted_data is not None:
            if hostname in decrypted_data:
                cookie_str = ""
                keys_matched = []
                for value in decrypted_data[hostname]:
                    if keys is None or value['name'] in keys:
                        keys_matched.append(value['name'])
                        cookie_str += value['name'] + '=' + value['value'] + '; '
                if all_keys_required and keys is not None:
                    if collections.Counter(keys) == collections.Counter(keys_matched):
                        return cookie_str
                    else:
                        return None
                else:
                    return cookie_str
        return None

    def update_cookie(self, cookie: Dict[str, Any]) -> bool:
        """
        Update cookie data to CookieCloud.

        :param cookie: cookie value to update, if this cookie does not contain 'cookie_data' key, it will be added into 'cookie_data'.
        :return: if update success, return True, else return False.
        """
        if 'cookie_data' not in cookie:
            cookie = {'cookie_data': cookie}
        raw_data = json.dumps(cookie)
        encrypted_data = encrypt(raw_data.encode('utf-8'), self.get_the_key().encode('utf-8')).decode('utf-8')
        cookie_cloud_request = requests.post(urljoin(self.url, '/update'), data={'uuid': self.uuid, 'encrypted': encrypted_data})
        if cookie_cloud_request.status_code == 200:
            if cookie_cloud_request.json()['action'] == 'done':
                return True
        return False

    def get_the_key(self) -> str:
        """
        Get the key used to encrypt and decrypt data.

        :return: the key.
        """
        md5 = hashlib.md5()
        md5.update((self.uuid + '-' + self.password).encode('utf-8'))
        return md5.hexdigest()[:16]
