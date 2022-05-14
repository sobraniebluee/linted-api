from main import client
import os

TOKEN = ''


CURL_POST = f'curl -X POST -H "Content-Type: application/json" -d @reg.json http://localhost:5003/api/v.1.0/user/register'


def test_curl_reg():
    os.system(CURL_POST)


def test_register():
    data = {
        'email': 'd1imf31291@cqq.cr',
        'password': 'Front1529',
        'username': '111'
    }
    res = client.post('api/v.1.0/user/register', json=data)

    print(res.status_code)
    print(res.get_json())


def test_login():
    data = {
        'email': 'ddf',
        'username': 'hel3lodima',
        'password': 'ccc11dddddd'
    }
    res = client.post('api/v.1.0/user/login', json=data)

    print(res.status_code)
    print(res.get_json())