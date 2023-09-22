from config import config

from aiohttp import web

from mypackages.auxiliary import notifications

from config.setup_logging import setup_logging
from config.admin_panel import admin
from mypackages.usedesk.api import send_message, update_ticket

from utils.check_bearer import is_bearer_valid

logger = setup_logging(__name__)

WARNING_TEXT = f"ERROR! Bearer теперь инвалид!\n" \
               f"Введите:\n" \
               f"/sb скопированный_bearer"


async def new_ticket(request):
    logger.info('New ticket received')

    if not is_bearer_valid:
        last_bearer = admin.get_last_admin_bearer().strip()
        last_bearer_piece = f"{last_bearer[:20]}...{last_bearer[-20:]}"
        logger.warning(f'Invalid Bearer: {last_bearer_piece}')

        if notifications.send_tg_bot_warning_msg(WARNING_TEXT):
            logger.info('Sent a warning message to a telegram bot')
        return web.Response(status=500)

    try:
        # User data from ticket
        data = await request.json()
        if config.ASSEMBLING_MOD != 'DEV':
            ticket_id = data['ticket_id']
        else:
            ticket_id = config.TEST_TICKER
        user_id = admin.get_user_id(data["client_email"])
        user_birthday = admin.get_user(user_id)['birthday'].split()[0]

        # Unblocking the user in Leader-ID
        if not admin.is_user_blocked(user_id) and user_id != 1127536:
            logger.info('The user is not blocked')
            return web.Response(status=200)
        if config.ASSEMBLING_MOD != 'DEV':
            admin.unlocking_user(user_id, check_existence=False)
            admin.approve_user(user_id, check_existence=False)
        logger.info(f'User with ID {user_id} and date of birth {user_birthday} is unblocked')

        # Sending a response in Usedesk
        mistake_in_age = True if int(user_birthday[:4]) > 2012 else False
        if not mistake_in_age:
            text = """<p>Здравствуйте!</p>
        <p>Ваш профиль был деактивирован по причине того, что вы не загрузили сканы согласий родителей на обработку ваших персональных данных в свой профиль.<br/>
        Временно активировали ваш профиль и продлили срок для загрузки согласий на 30 дней.<br/>
        Пожалуйста, загрузите сканы согласий в разделе — <a href="https://leader-id.ru/settings?tab=privacy">https://leader-id.ru/settings?tab=privacy</a>, иначе ваш профиль будет вновь деактивирован. Шаблоны документов прикрепляем во вложения к письму.
        </p>
        <p>Подробности можно прочитать в статье:<br/>
        <a href="http://leader-id.usedocs.com/article/42745">Где заполнить согласие несовершеннолетнего на обработку персональных данных?</a>
        </p>
        <p>Если у вас остались вопросы, мы с радостью на них ответим.<br/>
        Служба поддержки Leader-ID.<br/>
        <a href="mailto:support@leader-id.ru">support@leader-id.ru</a>
        </p>
        <hr/>
        <p>Основные вопросы и ответы в разделе «<a href="http://leader-id.usedocs.com/">Частые вопросы</a>»</p>
        <hr/>
        <p>Вы можете написать в наш чат-бот <a href="https://t.me/leaderid_bot" target="_blank">Telegram</a></p>"""
            files = ["statics/files/Согласие на обработку персональных данных.docx",
                     "statics/files/Согласие на распространение персональных данных.docx"]
        else:
            text = """<p>Здравствуйте!</p>
<p>Ваш профиль был деактивирован, так как в настройках указан некорректный год рождения.<br/>
Мы активировали профиль, пожалуйста, измените дату рождения, перейдя по ссылке: <a href="https://leader-id.ru/settings?tab=main">https://leader-id.ru/settings?tab=main</a>.<br/>
<br/>
Просим вас пройти небольшой <a href="https://pnp.leader-id.ru/polls/p/67645e46-f179-45f1-8caf-50ec0bcd99c8/" target="_blank">опрос удовлетворенности поддержкой</a>. Это позволит нам улучшить ее качество.<br/>
<br/>
Если у вас остались вопросы, мы с радостью на них ответим.<br/>
Служба поддержки Leader-ID.<br/>
<a href="mailto:support@leader-id.ru">support@leader-id.ru</a>
</p>
<hr/>
<p>Основные вопросы и ответы в разделе «<a href="http://leader-id.usedocs.com/">Частые вопросы</a>»</p>
<hr/>
<p>Вы можете написать в наш чат-бот <a href="https://t.me/leaderid_bot" target="_blank">Telegram</a></p>"""
            files = []
        send_message(ticket=ticket_id, message=text, fls=files)
        logger.info(f'Automatic response to usedesk ticket sent')
        # Updating the ticket
        update_ticket(ticket=ticket_id, category_lid="Редактирование профиля")
        logger.info(f'Usedesk Ticket automatically updated')

        text = f'🔓 <a href="https://admin.leader-id.ru/users/{user_id}">{user_id}</a> ({user_birthday})'
        notifications.send_tg_bot_msg(text, no_notification=True)
        logger.info(f'Sent a message to a telegram bot')

        return web.Response(status=200)

    except Exception as e:
        logger.exception(f'{e}')
        return web.Response(status=500)
