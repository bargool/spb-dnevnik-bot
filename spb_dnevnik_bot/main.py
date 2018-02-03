import os
import logging
import argparse

from spb_dnevnik_bot import __about__


def main():
    """Parses command-line arguments and starts bot"""
    parser = argparse.ArgumentParser(description=__about__.__summary__)
    parser.add_argument('--version', action='version', version='%(prog)s ' + __about__.__version__)
    parser.add_argument('-d', '--debug', action='store_true', help='debug mode')
    parser.add_argument('token', help='telegram bot token')
    parser.add_argument('login', help='login')
    parser.add_argument('password', help='password')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    # bot will read config from environment
    os.environ['SPB_DNEVNIK_BOT_TOKEN'] = args.token
    os.environ['SPB_DNEVNIK_BOT_ESIA_LOGIN'] = args.login
    os.environ['SPB_DNEVNIK_BOT_ESIA_PASSWORD'] = args.password

    from spb_dnevnik_bot.bot import start_bot
    start_bot()


if __name__ == '__main__':
    main()
