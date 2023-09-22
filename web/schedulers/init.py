from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from web.schedulers.check_bearer import run_check_bearer
from web.schedulers.event_moderation import EventModeration
from web.schedulers.mailing_moderation import MailingModerator

from config.setup_logging import setup_logging
from config.admin_panel import admin
from config.redis import redis

logger = setup_logging(__name__)


async def init_schedulers(app):
    scheduler = AsyncIOScheduler()

    if not scheduler.running:
        start_time = datetime.now() + timedelta(seconds=20)

        scheduler.add_job(
            run_check_bearer,
            'interval',
            minutes=9,
            id='check',
            coalesce=True,
            max_instances=1,
            kwargs={'scheduler': scheduler, 'admin_panel': admin},
            next_run_time=start_time,
        )

        scheduler.add_job(
            EventModeration(admin_panel=admin).run_event_moderation,
            'interval',
            minutes=149,
            id='event_moderation_by_bearer',
            coalesce=True,
            max_instances=1,
            next_run_time=start_time,
        )

        scheduler.add_job(
            MailingModerator(redis_client=redis, admin_panel=admin).run_mailing_moderator,
            'interval',
            minutes=150,
            id='mailing_moderation_by_bearer',
            coalesce=True,
            max_instances=1,
            next_run_time=start_time,
        )

        logger.info(f'Initializing the Scheduler')
        scheduler.start()

        app['scheduler'] = scheduler
