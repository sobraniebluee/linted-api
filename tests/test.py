import os
import random
import string
import time
from main import client
from flask_jwt_extended import get_jwt_identity, get_jwt_header


TOKENS = \
    {'access_token':
         'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjU3MjAyNCwianRpIjoiYmQzYzlkYWItMzQ3Yy00ZTJiLTk0NjYtMTA2NmMzMDk0YmZjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImZkOWYxYzZiLTMxMTQtNDE4NS1hZjUwLWYzOGJhOTQ2OTg3MyIsIm5iZiI6MTY1MjU3MjAyNCwiZXhwIjoxNjUyNTcyMDg0fQ.c7S93BGUne2lb8as1hrbjnl5X58YQZARtC0l8WjAU7w',
     'refresh_token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjU3MjAyNCwianRpIjoiMWEwMDQwMGMtNGQ5ZC00MmM0LWE5YmMtN2RlODVmZDEzYzBhIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiJmZDlmMWM2Yi0zMTE0LTQxODUtYWY1MC1mMzhiYTk0Njk4NzMiLCJuYmYiOjE2NTI1NzIwMjQsImV4cCI6MTY1NTE2NDAyNH0.DMQHUOCET63C1viiOWfVTPA966sQfbT3jOgJPQXrFNo'}

access_token =\
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY1MjU4MDM3NCwianRpIjoiNmJjMjJiZDUtZWMxOS00OTllLTg4M2ItNmFlNjZkYjk5NWIxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImU4ZWUxNGJiLTQ5NDYtNDI0ZS05ZWY3LWJjZDk4ZWRhZWFlOSIsIm5iZiI6MTY1MjU4MDM3NCwiZXhwIjoxNjUyNTgyMTc0fQ.kZf0vzIEqNF2dSFpcDYV7ui51lQJ31ipAXfC0OIs5OU",

CURL_POST = f'curl -X POST -H "Content-Type: application/json" -d @reg.json http://127.0.0.1:5003/api/v.1.0/user/register'


def test_curl_reg():
    res = os.system(CURL_POST)
    print(res)


def test_register(data):
    random_email = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(12)])
    # data = {
    #     'email': f'{random_email}@{random_email}.com',
    #     'password': 'Front1529',
    #     'username': f'{random_email}{str(time.time())}'
    # }
    res = client.post('api/v.1.0/user/register', json=data)
    print(res.get_json())
    print(res.status_code)
    return res.status_code

def test_login(data):
    # data = {
    #     'email': f'dissssm2f292q1@ms2ss.csom',
    #     'password': 'Front1529',
    # }
    res = client.post('api/v.1.0/user/login', json=data)

    print(res.get_json())
    return res.status_code


def test_refresh_token():
    headers = {
        'Authorization': f"Bearer {TOKENS['refresh_token']}"
    }
    res = client.get('api/v.1.0/user/token/refresh', headers=headers)

    print(res.status_code)
    jwt = res.get_json()
    print(jwt)



def test_prot():
    headers = {
        'Authorization': f"Bearer {access_token}"
    }
    res = client.get('api/v.1.0/user/protected', headers=headers)
    print(res.status_code)
    print(res.get_json())



def test_login_register():
    random_email = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(12)])
    data = {
        'email': f'{random_email}@{random_email}.com',
        'password': 'Front1529',
        'username': f'{random_email}{str(time.time())}'
    }
    res_reg = test_register(data)
    res_log = test_login(data={'username': data['username'], 'password': 'Front1529'})
    assert res_reg == 200
    assert res_log == 200

    # res_log = test_login(data={'username': data['username'], 'password': 'Front1529'})
    # res_log = test_login(data={'username': data['username'], 'password': 'Front1529'})
def test_def_1():
    COUNT = 0
    while COUNT < 100:
        test_login_register()

        COUNT = COUNT + 1
        if COUNT == 1000:
            break
    print(COUNT)


