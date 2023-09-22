import json
from datetime import datetime

from bot.aiohttp_server.app import init_app
from config import config

import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.filters import CommandObject, Command
from aiogram.webhook.aiohttp_server import setup_application

from aiohttp import web

from mypackages import leader_id

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

ALLOWED_CHATS_ID = [config.MY_CHAT_ID, config.TEAM_CHAT_ID]
ALLOWED_CHATS_ID = [int(chat_id) for chat_id in ALLOWED_CHATS_ID]

router = Router()


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{config.WEBHOOK_URL}{config.WEBHOOK_PATH}", secret_token=config.WEBHOOK_SECRET)
    await set_commands(bot)


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/help", description="Помощь"),
    ]
    await bot.set_my_commands(commands)


async def del_message(message: types.Message, daley: float = 0):
    await asyncio.sleep(daley)
    await message.delete()


@router.message(Command(commands=["help"]))
async def unloading_list(message: types.Message):
    await del_message(message)
    await message.answer(f'1️⃣ /set_bearer или /sb\n'
                         f'Задать новый bearer\n'
                         f'\n',
                         disable_notification=True,
                         parse_mode="html")


@router.message(Command(commands=["set_bearer", "sb"]))
async def set_bearer(message: types.Message, command: CommandObject):
    await del_message(message)

    if not command.args:
        text = f'Если бот выбило из админки Leader-ID, скопируйте свой bearer и отправьте боту:\n' \
               f'Пример: /sb eyJIiJ9.eyJQ3er3...'
        await message.answer(text)

    else:
        old_bearer = leader_id.AdminPanel.get_last_admin_bearer()
        print(f'[{datetime.now()}][*] Old bearer: "{old_bearer[:15]}..."')
        bearer = command.args.replace('Bearer', '').strip()
        leader_id.AdminPanel.save_new_admin_bearer(bearer)

        try:
            admin = leader_id.AdminPanel()
            if admin.is_admin_bearer_valid():
                print(f'A NEW bearer has been assigned: "{admin.get_last_admin_bearer().strip()}"')
                text = f"Ваше превосходительство, Bearer, который Вы были добры предоставить, " \
                       f"оказался подходящим. Это весьма отрадно, если позволите заметить."
                await message.answer(text)
            else:
                raise
        except Exception as e:
            print(f'[{datetime.now()}][!] Ошибка Bearer инвалид! {e}')
            text = f"Error! Bearer инвалид!\n" \
                   f"Введите:\n" \
                   f"/sb скопированный_bearer"
            answer = await message.answer(text)
            await del_message(answer, 4)


# @router.message()
# async def echo_handler(message: types.Message) -> None:
#     print(message.text)
#     if 'bearer' in message.text.lower():
#         await del_message(message, 4)


def main():
    bot = Bot(token=config.BOT_TOKEN)

    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)

    router.message.filter(F.chat.id.in_(set(ALLOWED_CHATS_ID)))

    app = init_app(dp, bot, config.WEBHOOK_SECRET)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=config.SERVER_HOST, port=config.BOT_PORT)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
