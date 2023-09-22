from datetime import datetime, timedelta

from config import config

import json
import requests

from requests import post

URL_SEND_MSG = f'https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/53.0.2785.143 Safari/537.36',
    "Content-Type": "application/json"
}

last_call = None


def send_tg_bot_warning_msg(text, chat_id=config.TEAM_CHAT_ID, delay_sec=2000) -> bool:
    global last_call

    is_message_sent = False

    message = {"chat_id": chat_id,
               "text": text,
               "parse_mode": "HTML"}
    if last_call is None or datetime.now() > last_call + timedelta(seconds=delay_sec):
        post(URL_SEND_MSG, data=json.dumps(message), headers=headers)
        last_call = datetime.now()
        is_message_sent = True

    return is_message_sent


def send_tg_bot_msg(text, chat_id=config.TEAM_CHAT_ID, no_preview=True, no_notification=False) -> requests.Response:
    message = {"chat_id": chat_id,
               "text": text,
               "disable_web_page_preview": no_preview,
               "disable_notification": no_notification,
               "parse_mode": "HTML"}
    res = post(URL_SEND_MSG, data=json.dumps(message), headers=headers)
    return res


def send_tg_bot_start_msg(text, chat_id=config.MY_CHAT_ID) -> requests.Response:
    message = {"chat_id": chat_id,
               "text": text,
               "parse_mode": "HTML"}
    return post(URL_SEND_MSG, data=json.dumps(message), headers=headers)
