import os
from datetime import datetime

from mypackages import auxiliary

import json
from requests import exceptions, Session
from requests.models import Response
from time import time, sleep
from typing import Union

import redis

from dotenv import load_dotenv

load_dotenv()

r = redis.Redis(host='redis', port=6379, db=0, password=os.getenv('REDIS_PASSWORD'))

SECOND_ADMIN_LOGIN = os.getenv("SECOND_ADMIN_LOGIN")
SECOND_ADMIN_PASSWORD = os.getenv("SECOND_ADMIN_PASSWORD")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
HOST_V3 = 'https://leader-id.ru/api/v4/api/v3'
HOST_V4 = 'https://leader-id.ru/api/v4'


# Decorators
def request_repeater(fun):
    def wrapper(*args, **kwargs):
        retries = 5
        while True:
            try:
                start = time()
                res = fun(*args, **kwargs)
                auxiliary.set_delay(start)
                if res.ok is False:
                    print(f'[{datetime.now()}][!] {res.json()}')
                return res

            except exceptions.ConnectionError as exc:
                print(f'ConnectionError ({5 + 1 - retries})', end=' ')
                if retries == 0:
                    raise exc
                retries -= 1
                sleep(0.5)

    return wrapper


class AdminPanel:
    def __init__(self):
        self.sess = Session()
        self.set_last_admin_bearer()
        if not self.is_admin_bearer_valid():
            self.set_admin_bearer()
            if self.is_admin_bearer_valid() is True:
                print(f"[{datetime.now()}][+] Admin bearer updated")
                print(f"[{datetime.now()}][*] New bearer: ", self.get_last_admin_bearer().strip())
            else:
                print(f'[{datetime.now()}][!] Bearer auto updating... ERROR')

    @staticmethod
    def get_last_admin_bearer() -> str:
        token = r.get("bearer")
        if token is not None:
            return token.decode("utf-8")
        else:
            return ''

    def set_last_admin_bearer(self):
        self.sess.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 ',
            'authorization': f"Bearer {self.get_last_admin_bearer().strip()}"
        })

    def is_admin_bearer_valid(self) -> bool:
        self.set_last_admin_bearer()

        @request_repeater
        def res():
            url = HOST_V4 + '/admin/users?paginationSize=1000&query=1127536'
            return self.sess.get(url)

        return res().ok

    def get_admin_bearer(self) -> str:
        print(f"[{datetime.now()}][?] Trying to update an expired bearer...")

        @request_repeater
        def res():
            url = 'https://admin.leader-id.ru/api/v4/auth/login'
            data = {
                'email': SECOND_ADMIN_LOGIN,
                'password': SECOND_ADMIN_PASSWORD
            }
            return self.sess.post(url, data=json.dumps(data))

        res = res()
        if res.ok:
            return res.json()['data']['access_token']

    def set_admin_bearer(self):
        bearer = self.get_admin_bearer()

        if not bearer:
            return False

        self.sess.headers.update({
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 ',
            'authorization': f"Bearer {bearer}"
        })
        self.save_new_admin_bearer(bearer)
        return True

    @staticmethod
    def save_new_admin_bearer(bearer):
        r.set("bearer", bearer)

    def search_users(self, query: Union[str, int]) -> list:
        if isinstance(query, str):
            q = query.lower()

        @request_repeater
        def res():
            url = HOST_V4 + f'/admin/users?query={q}&paginationSize=1&paginationPage=1'
            return self.sess.get(url)

        return res().json()['data']['_items']

    def search_deleted_users(self, query):  # 0
        @request_repeater
        def res():
            url = HOST_V4 + f'/admin/users?query={query}&paginationSize=1000&status[]=0'
            return self.sess.get(url)

        return res().json()['data']['_items']

    def get_user(self, user) -> dict:
        @request_repeater
        def res():
            if isinstance(user, str):
                user_id = self.search_users(user)[0]['id']
            else:
                user_id = user

            url = HOST_V4 + f'/admin/users/{user_id}'
            return self.sess.get(url)

        return res().json()['data']

    def get_user_id(self, user_email: str):
        user = self.search_users(user_email)
        if not user:
            raise Exception(f'User {user_email} not found')
        return user[0]['id']

    def is_user_blocked(self, user):
        if isinstance(user, str):
            user_id = self.search_users(user)[0]['id']
        else:
            user_id = user

        return self.get_user(user_id)['status'] in [8, 9]

    def get_user_token(self, user_id) -> str:
        @request_repeater
        def res():
            url = HOST_V4 + '/admin/users/auth'
            data = {'userId': user_id}
            return self.sess.post(url, data=json.dumps(data))

        return res().json()['data']['token']

    def get_user_headers(self, user_id) -> dict:
        return {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/53.0.2785.143 Safari/537.36 ',
            'authorization': f"Bearer {self.get_user_token(user_id)}"
        }

    def get_user_session(self, user_id) -> Session:
        sess = Session()
        sess.headers.update(self.get_user_headers(user_id))
        return sess

    @request_repeater
    def unlocking_user(self, user: Union[int, str], check_existence=True) -> Response:
        if check_existence or isinstance(user, str):
            user_id = self.search_users(user)[0]['id']
        else:
            user_id = user

        data = {"userId": user_id}
        url = HOST_V4 + '/admin/users/refresh-verification-profile'
        return self.sess.post(url, data=json.dumps(data))

    @request_repeater
    def approve_user(self, user: Union[int, str], check_existence=True) -> Response:
        if check_existence or isinstance(user, str):
            user_id = self.search_users(user)[0]['id']
        else:
            user_id = user

        data = {"userId": user_id}
        url = HOST_V4 + '/admin/users/approve-profile'
        return self.sess.post(url, data=json.dumps(data))

    def get_events(self, format):
        url = HOST_V4 + f'/admin/events/search?format={format}&moderation=wait&sort=update'
        res = self.sess.get(url)
        return res.json()

    # 10 Черновик 20 На рассмотрении 30 Принято. Ожидает отправки.
    # 40 Выполняется отправка 50 Отправлено 60 Отклонено 70 Остановлено
    @request_repeater
    def unloading_mailing(self, status=20) -> Response:
        url = HOST_V4 + f'/admin/mailings?status={status}&paginationPage=1&paginationSize=1000'
        return self.sess.get(url)
