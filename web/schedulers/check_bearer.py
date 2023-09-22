from mypackages.auxiliary import notifications
from web.schedulers.jobs_control import pause_jobs_like, resume_jobs_like

from utils.check_bearer import is_bearer_valid

from config.setup_logging import setup_logging

logger = setup_logging(__name__)

WARNING_TEXT = f"Error, bearer инвалид!\n" \
               f"Введите:\n" \
               f"/sb скопированный_bearer"


def run_check_bearer(scheduler, admin_panel) -> None:
    logger.info('Check Bearer job started...')

    is_valid = is_bearer_valid(admin_panel)
    status_text = "TRUE" if is_valid else "FALSE"
    logger.info(f'Bearer validation: {status_text}')

    if not is_valid:
        last_bearer = admin_panel.get_last_admin_bearer().strip()
        last_bearer_piece = f"{last_bearer[:20]}...{last_bearer[-20:]}"
        logger.warning(f'Invalid Bearer: {last_bearer_piece}')

        if notifications.send_tg_bot_warning_msg(WARNING_TEXT):
            logger.info('Sent a warning message to a telegram bot')

        stopped_jobs = pause_jobs_like(scheduler, job_id_like='bearer')
        if stopped_jobs:
            logger.warning(f'Jobs like "bearer" were stopped: {stopped_jobs}')
    else:
        resumed_jobs = resume_jobs_like(scheduler, job_id_like='bearer')
        if resumed_jobs:
            logger.info(f'Jobs like "bearer" were resumed: {resumed_jobs}')

    logger.info('Check Bearer job completed')
