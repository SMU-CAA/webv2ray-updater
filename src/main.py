import os
from io import BytesIO
import time

import requests
from bs4 import BeautifulSoup
from ai.predict import Predict

requests.packages.urllib3.disable_warnings()

p = Predict()

s = requests.session()
s.verify = False

SHMTU_CAS_USERNAME = os.getenv('SHMTU_CAS_USERNAME')
SHMTU_CAS_PASSWORD = os.getenv('SHMTU_CAS_PASSWORD')
WEBV2RAY_UPDATE_TOKEN = os.getenv('WEBV2RAY_UPDATE_TOKEN')
V2RAY_PATH = os.getenv('V2RAY_PATH')

MAX_RETRY = 3
BASE_URL = 'https://webvpn.shmtu.edu.cn'
CAS_PATH = '/https/77726476706e69737468656265737421f3f652d2343865446b468ca88d1b203b'

request_headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
                  ' AppleWebKit/537.36 (KHTML, like Gecko)'
                  ' Chrome/96.0.4664.110 Safari/537.36'
}


def webvpn_login(username, password):
    # get csrf token
    login_url = '{}{}/cas/login'.format(BASE_URL, CAS_PATH)
    prelogin_res = s.get(login_url, headers=request_headers)
    prelogin_soup = BeautifulSoup(prelogin_res.text, 'html.parser')
    csrf_token = prelogin_soup.select('input[name=execution]')[0].get('value')

    # get captcha image
    captcha_url = '{}{}/cas/captcha'.format(
        BASE_URL, CAS_PATH)
    captcha = s.get(captcha_url, headers=request_headers)
    captcha_prediction = p.get_prediction(BytesIO(captcha.content))

    # submit login info
    payload = {
        'username': username,
        'password': password,
        'validateCode': captcha_prediction[1],
        'execution': csrf_token,
        '_eventId': 'submit'
    }
    login_res = s.post(login_url, headers=request_headers, data=payload)

    # redirect to webvpn
    redirect_url = "{}{}/cas/login?service=https%3A%2F%2Fwebvpn.shmtu.edu.cn%2Flogin%3Fcas_login%3Dtrue".format(
        BASE_URL, CAS_PATH)
    redirect_res = s.get(redirect_url, headers=request_headers)

    # return 'WebVPN门户' in redirect_res.text
    return 'Bad Request' in redirect_res.text  # 似乎跟随了之前访问的页面


def valid_state():
    valid_url = "{}/".format(BASE_URL, V2RAY_PATH)
    valid_res = s.get(valid_url, headers=request_headers)

    # vmess + ws works if 'Bad Request' show up
    return 'Bad Request' in valid_res.text


def log_time():
    return '{} '.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))


if __name__ == '__main__':
    retry_count = 0
    while True:
        valid = valid_state()
        if not valid:
            print('{}检测到一次失败，等待重试'.format(log_time()))
            if retry_count % MAX_RETRY == 0:
                login = webvpn_login(SHMTU_CAS_USERNAME, SHMTU_CAS_PASSWORD)
                if login:
                    print('{}登录成功'.format(log_time()))
                    cookies = s.cookies.get_dict()
                    print('{}{}'.format(log_time(), cookies))
                    ticket = cookies['wengine_vpn_ticket']
                    ticket_update = requests.post(
                        'https://webv2ray.shmtu.org/?ticket={}&token={}'.format(ticket, WEBV2RAY_UPDATE_TOKEN))
                else:
                    print('{}登录失败'.format(log_time()))
            retry_count += 1
        time.sleep(10)
