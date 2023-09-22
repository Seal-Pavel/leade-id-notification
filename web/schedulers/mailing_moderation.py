import json

from mypackages.auxiliary import notifications

from config.setup_logging import setup_logging

logger = setup_logging(__name__)


class MailingModerator:
    def __init__(self, redis_client, admin_panel):
        self.redis_client = redis_client
        self.admin_panel = admin_panel
        self.redis_key = 'unconsidered_mailings'

    def _get_unconsidered_mailings(self) -> list[dict]:
        unconsidered_mailings: list[dict] = self.admin_panel.unloading_mailing(status=20).json()['data']['_items']
        if unconsidered_mailings:
            for mailing in unconsidered_mailings:
                if 'events' in mailing:
                    del mailing['events']
        return unconsidered_mailings

    def _add_redis(self, unconsidered_mailings: list[dict]):
        for mailing in unconsidered_mailings:
            self.redis_client.sadd(self.redis_key, json.dumps(mailing))

    def _get_redis(self) -> list[str]:
        mailings = self.redis_client.smembers(self.redis_key)
        return [mailing.decode('utf-8') for mailing in mailings]

    @staticmethod
    def notify_about_new_mailings(mailings: list[dict]):
        new_mailings_links = '\n'.join([f'https://admin.leader-id.ru/mailing/{mailing["id"]}' for mailing in mailings])
        text = f'📩 Новые рассылки, требующие вашего внимания:\n{new_mailings_links}'
        notifications.send_tg_bot_msg(text)

    def run_mailing_moderator(self):
        logger.info('Mailing moderation job started...')

        try:
            unconsidered_mailings = self._get_unconsidered_mailings()

            if not unconsidered_mailings:
                logger.info('All mailings were moderated')
                return

            old_mailings = [json.loads(m) for m in self._get_redis()]
            self._add_redis(unconsidered_mailings)
            all_mailings = [json.loads(m) for m in self._get_redis()]

            new_mailings = [m for m in all_mailings if m not in old_mailings]

            if not new_mailings:
                logger.info('There are no NEW mailings')
                return

            self.notify_about_new_mailings(new_mailings)
            logger.info(f'Sent a message to a telegram bot')

        except Exception as e:
            logger.exception(f'Telegram bot message FAILED: {e}')

        finally:
            logger.info('Mailing moderation job completed')
