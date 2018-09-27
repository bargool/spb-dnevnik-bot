import logging
from datetime import timedelta, date

from requests.exceptions import Timeout
from selenium.common.exceptions import TimeoutException
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler

from .__about__ import __version__
from .parser import Parser

logging.getLogger('urllib3').propagate = False

logger = logging.getLogger(__name__)


HELP_MESSAGE = f'''
Данный бот служит для информирования о событиях на сайте https://petersburgedu.ru,
если конкретно, то об оценках и домашних заданиях.
Список команд:
/help - Повторить данное сообщение
/yesterday - Информация по вчерашнему дню
/today - Информация за сегодня
/tomorrow - Информация по завтрашнему дню
Версия бота: {__version__}
'''.strip()


def send_welcome(bot, update: Update) -> None:
    logger.info("Got welcome message from user %s", update.message.from_user)
    bot.send_message(chat_id=update.message.chat_id, text=HELP_MESSAGE)


def get_yesterday(bot, update: Update) -> None:
    create_message(bot, update, diary_date=date.today() - timedelta(days=1))


def get_today(bot, update: Update) -> None:
    create_message(bot, update, diary_date=date.today())


def get_tomorrow(bot, update: Update) -> None:
    create_message(bot, update, diary_date=date.today() + timedelta(days=1))


def create_message(bot, update: Update, diary_date: date) -> None:
    chat_id = update.message.chat_id
    bot.send_message(chat_id, "Подождите...")
    bot.send_chat_action(chat_id, 'typing')
    if diary_date.weekday() == 6:
        diary_date += timedelta(days=1)
    try:
        # bot.session.login()
        parser = Parser(bot.session, diary_date)
        weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
        messages = ["Информация по _{}, {}_".format(diary_date.strftime('%d.%m.%Y'),
                                                    weekdays[diary_date.weekday()]),
                    "```text"]
        for idx, lesson in enumerate(parser.get_diary(), 1):
            name = lesson.name or 'Нет урока'
            if lesson.mark or lesson.homework:
                mark = lesson.mark or '-'
                hw = lesson.homework or '-'
                m = f'{idx}. {name}: отм: {mark}; д/з: {hw}'
            else:
                m = f'{idx}. {name}'
            messages.append(m)
        messages.append("```")
        bot.send_message(chat_id, "\n".join(messages), parse_mode='Markdown')
    except (TimeoutException, Timeout):
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте позже")
        logger.exception("Ошибка при обработке запроса %s", update.message)
    except Exception:
        bot.send_message(chat_id, "Произошла ошибка")
        logger.exception("Ошибка при обработке запроса %s", update.message)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler('start', send_welcome))
    dispatcher.add_handler(CommandHandler('help', send_welcome))
    dispatcher.add_handler(CommandHandler('today', get_today))
    dispatcher.add_handler(CommandHandler('tomorrow', get_tomorrow))
    dispatcher.add_handler(CommandHandler('yesterday', get_yesterday))
