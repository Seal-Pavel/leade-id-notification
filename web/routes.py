from web.views.new_ticket import new_ticket
from web.views.index import index


def init_routes(app):
    app.router.add_get('/', index)
    app.router.add_post('/api/v1/newTicket', new_ticket)
