from aiohttp import web

from web.routes import init_routes
from web.schedulers.init import init_schedulers


async def init_app() -> web.Application:
    app = web.Application()
    app.on_startup.append(init_schedulers)
    init_routes(app)
    return app
