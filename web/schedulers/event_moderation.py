import requests

from mypackages.auxiliary import notifications

from config.setup_logging import setup_logging

logger = setup_logging(__name__)


class EventModeration:
    def __init__(self, admin_panel):
        self.admin_panel = admin_panel

    def _get_online_events_links(self) -> list:
        events: list = self.admin_panel.get_events(format='online')['data']['_items']
        return [f"https://admin.leader-id.ru/events/{event['id']}" for event in events if not event['space_id']]

    def _get_not_in_tk_events_links(self) -> list:
        events: list = self.admin_panel.get_events(format='place')['data']['_items']
        return [f"https://admin.leader-id.ru/events/{event['id']}" for event in events if not event['space_id']]

    @staticmethod
    def notify_about_new_events(event_links) -> requests.Response:
        event_links = '\n'.join(event_links)
        text = f'👀 Мероприятия, требующие вашего внимания:\n{event_links}'
        res = notifications.send_tg_bot_msg(text)
        return res

    def run_event_moderation(self):
        logger.info('Event moderation job started...')

        try:
            event_links = self._get_online_events_links() + self._get_not_in_tk_events_links()

            if not event_links:
                logger.info('All events were moderated')
                return

            self.notify_about_new_events(event_links)
            logger.info(f'Sent a message to a telegram bot')

        except Exception as e:
            logger.exception(f'Telegram bot message FAILED: {e}')

        finally:
            logger.info('Event moderation job completed')
