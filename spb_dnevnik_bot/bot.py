import logging
import os
from datetime import timedelta, date

import telebot
from selenium.common.exceptions import TimeoutException

from spb_dnevnik_bot.__about__ import __version__
from spb_dnevnik_bot.parser import Parser, EsiaSession, RegularSession

logging.getLogger('urllib3').propagate = False

logger = logging.getLogger(__name__)

TOKEN = os.environ.get('SPB_DNEVNIK_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)


ESIA_LOGIN = os.environ.get('SPB_DNEVNIK_BOT_ESIA_LOGIN')
ESIA_PASSWORD = os.environ.get('SPB_DNEVNIK_BOT_ESIA_PASSWORD')

# TODO: Handle admins

HELP_MESSAGE = f'''
Данный бот служит для информирования о событиях на сайте https://petersburgedu.ru,
если конкретно, то об оценках и домашних заданиях.
Список команд:
/help - Повторить данное сообщение
/today - Информация за сегодня
/tomorrow - Информация по завтрашнему дню
Версия бота: {__version__}
'''.strip()


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: 'telebot.types.Message') -> None:
    logger.info("Got welcome message from user %s", message.from_user)
    bot.send_message(message.chat.id, HELP_MESSAGE)


@bot.message_handler(commands=['marks', ])
def get_marks(message: 'telebot.types.Message') -> None:
    bot.send_message(message.chat.id, "Я пока не научился отвечать на эту команду")


@bot.message_handler(commands=['homeworks', ])
def get_homeworks(message: 'telebot.types.Message') -> None:
    bot.send_message(message.chat.id, "Я пока не научился отвечать на эту команду")


@bot.message_handler(commands=['today', ])
def get_today(message: 'telebot.types.Message') -> None:
    create_message(message, diary_date=date.today())


@bot.message_handler(commands=['tomorrow', ])
def get_tomorrow(message: 'telebot.types.Message') -> None:
    create_message(message, diary_date=date.today() + timedelta(days=1))


def create_message(message: 'telebot.types.Message', diary_date: date) -> None:
    chat_id = message.chat.id
    bot.send_message(chat_id, "Подождите...")
    bot.send_chat_action(chat_id, 'typing')
    if diary_date.weekday() == 6:
        diary_date += timedelta(days=1)
    try:
        session = RegularSession(ESIA_LOGIN, ESIA_PASSWORD)
        session.login()
        parser = Parser(session, diary_date)
        weekdays = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота']
        messages = ["Информация по _{}, {}_".format(diary_date.strftime('%d.%m.%Y'),
                                                    weekdays[diary_date.weekday()]),
                    "```text"]
        for idx, l in enumerate(parser.get_diary(), 1):
            name = l.name or 'Нет урока'
            if l.mark or l.homework:
                mark = l.mark or '-'
                hw = l.homework or '-'
                m = f'{idx}. {name}: отм: {mark}; д/з: {hw}'
            else:
                m = f'{idx}. {name}'
            messages.append(m)
        messages.append("```")
        bot.send_message(chat_id, "\n".join(messages), parse_mode='Markdown')
    except TimeoutException:
        bot.send_message(chat_id, "Произошла ошибка, сайт дневника отвечает медленно. Попробуйте позже")
        logger.exception("Ошибка при обработке запроса %s", message)
    except:
        bot.send_message(chat_id, "Произошла ошибка")
        logger.exception("Ошибка при обработке запроса %s", message)


def start_bot() -> None:
    logger.info(bot.get_me())
    logger.info("Waiting for messages")
    bot.polling()


if __name__ == '__main__':
    start_bot()
