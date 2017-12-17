import logging

from spb_dnevnik_bot.bot import bot


def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info(bot.get_me())
    logging.info("Waiting for messages")
    bot.polling()


if __name__ == '__main__':
    main()
