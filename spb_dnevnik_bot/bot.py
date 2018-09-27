import logging

from telegram import Bot
from telegram.ext import Updater

from .parser import EsiaSession, RegularSession
from .message_handlers import register_handlers

logger = logging.getLogger(__name__)


class DnevnikBot(Bot):

    def __init__(self, token, base_url=None, base_file_url=None, request=None, private_key=None,
                 private_key_password=None, session=None):
        super().__init__(token, base_url, base_file_url, request, private_key, private_key_password)
        self.session = session


def create_updater(args) -> Updater:
    session_cls = EsiaSession if args.esia else RegularSession
    session = session_cls(args.login, args.password)
    session.login()
    bot = DnevnikBot(token=args.token, session=session)
    updater = Updater(bot=bot)
    register_handlers(updater.dispatcher)
    return updater


def start_updater(updater: Updater) -> None:
    logger.info(updater.bot.get_me())
    logger.info("Waiting for messages")
    updater.start_polling()
