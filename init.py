import requests

from config import config
from mypackages.auxiliary import notifications


def set_init_values():
    pass


def send_start_message_in_tg(text='===START===') -> requests.Response:
    return notifications.send_tg_bot_start_msg(text)


def main():
    text = f'\n\n\n===START=== ({config.ASSEMBLING_MOD})'
    if config.ASSEMBLING_MOD == 'DEV':
        text += '\n!_DEVELOP_MOD_!'
    print(text)

    set_init_values()
    send_start_message_in_tg(text)


if __name__ == '__main__':
    main()
