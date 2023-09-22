from aiogram.webhook.aiohttp_server import SimpleRequestHandler
from config import config


def init_routes(app, dp, bot, secret_token):
    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=secret_token
    )
    webhook_requests_handler.register(app, path=config.WEBHOOK_PATH)
