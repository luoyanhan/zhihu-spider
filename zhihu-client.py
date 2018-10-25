import requests
import base64
from urllib.parse import urlencode
from PIL import Image
import hashlib
import hmac
import time
import pickle

CLIENT_ID = '8d5227e0aaaa4797a763ac64e0c3b8'
ZHIHU_API_ROOT = 'https://api.zhihu.com'
CAPTCHA_URL = ZHIHU_API_ROOT + '/captcha'
DEFAULT_UA = 'Futureve/4.18.0 Mozilla/5.0 (Linux; Android 6.0; ' \
             'Google Nexus 5 - 6.0.0 - API 23 - 1080x1920 Build/MRA58K; wv) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 ' \
             'Chrome/44.0.2403.119 Mobile Safari/537.36 ' \
             'Google-HTTP-Java-Client/1.22.0 (gzip)'
UUID = 'AHBCVBVCDAtLBfZCo1SYbPj8SgivYjqcGCs='
APP_BUILD = 'release'
APP_VERSION = '4.18.0'
APP_SECRET = 'ecbefbf6b17e47ecb9035107866380'
API_VERSION = '3.0.54'
APP_ZA = urlencode({
    'OS': 'Android',
    'Release': '6.0',
    'Model': 'Google Nexus 5 - 6.0.0 - API 23 - 1080x1920',
    'VersionName': APP_VERSION,
    'VersionCode': '477',
    'Width': '1080',
    'Height': '1920',
    'Installer': 'Google Play',
})
CAPTCHA_URL = ZHIHU_API_ROOT + '/captcha'
LOGIN_URL = ZHIHU_API_ROOT + '/sign_in'
SELF_DETAIL_URL = ZHIHU_API_ROOT + '/people/self'


LOGIN_DATA = {
    'grant_type': 'password',
    'source': 'com.zhihu.android',
    'client_id': '',
    'signature': '',
    'timestamp': '',
    'username': '',
    'password': '',
}

headers = {}
headers['x-api-version'] = API_VERSION
headers['x-app-version'] = APP_VERSION
headers['x-app-build'] = APP_BUILD
headers['x-app-za'] = APP_ZA
headers['x-uuid'] = UUID
headers['User-Agent'] = DEFAULT_UA
headers['Authorization'] = 'oauth {0}'.format(CLIENT_ID)



class ZhihuClient:
    def __init__(self, client_id=None, secret=None):
        self._session = requests.session()
        self._client_id = client_id or CLIENT_ID
        self._secret = secret or APP_SECRET

    def need_captcha(self):
        response = self._session.get(CAPTCHA_URL, headers=headers)
        try:
            result = response.json()
            return result['show_captcha']
        except:
            pass

    def get_captcha(self):
        if self.need_captcha():
            response = self._session.put(CAPTCHA_URL, headers=headers)
            try:
                result = response.json()
                # img = base64.decodebytes(result['img_base64'].encode('utf-8'))
                img = base64.b64decode(result['img_base64'].encode('utf-8'))
                with open('a.png', 'wb') as f:
                    f.write(img)
                img = Image.open('a.png')
                img.show()
            except:
                pass
        return None

    def login_signature(self, data, secret):

        data['timestamp'] = str(int(time.time()))
        params = ''.join([
            data['grant_type'],
            data['client_id'],
            data['source'],
            data['timestamp'],
        ])
        data['signature'] = hmac.new(
            secret.encode('utf-8'),
            params.encode('utf-8'),
            hashlib.sha1
        ).hexdigest()

    def login(self, username, password, captcha=None):
        if captcha is None:
            if self.need_captcha():
                self.get_captcha()
                captcha = input('please input captcha:')
        response = self._session.post(CAPTCHA_URL, headers=headers, data={'input_text': captcha})
        if 'error' in response:
            return False, response['error']['message']
        data = dict(LOGIN_DATA)
        data['username'] = username
        data['password'] = password
        data['client_id'] = self._client_id
        self.login_signature(data, self._secret)
        response = self._session.post(LOGIN_URL, headers=headers, data=data)
        response = response.json()
        headers['Authorization'] = '{type} {token}'.format(
            type=str(response['token_type'].capitalize()),
            token=str(response['access_token'])
        )
        res = self._session.get(SELF_DETAIL_URL, headers=headers)
        print(res.text)




if __name__ == "__main__":
    client = ZhihuClient()
    client.login('+86phone_num', 'password')