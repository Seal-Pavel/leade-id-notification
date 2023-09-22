from aiohttp import web

from bot.aiohttp_server.routes import init_routes


def init_app(dp, bot, secret_token) -> web.Application:
    app = web.Application()
    init_routes(app, dp, bot, secret_token)
    return app
