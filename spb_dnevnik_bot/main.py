import argparse
import logging

from spb_dnevnik_bot import __about__
from spb_dnevnik_bot.bot import create_updater, start_updater


def main():
    """Parses command-line arguments and starts bot"""
    parser = argparse.ArgumentParser(description=__about__.__summary__)
    parser.add_argument('--version', action='version', version='%(prog)s ' + __about__.__version__)
    parser.add_argument('-d', '--debug', action='store_true', help='debug mode')
    parser.add_argument('token', help='telegram bot token')
    parser.add_argument('login', help='login')
    parser.add_argument('password', help='password')
    parser.add_argument('--esia', action='store_true', help='use ESIA auth instead of regular')
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)

    updater = create_updater(args)
    start_updater(updater)


if __name__ == '__main__':
    main()
