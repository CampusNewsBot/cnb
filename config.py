import logging

DEBUG = False
DEBUG_NO_SEND = False

telegram_url = 'https://api.telegram.org/bot{}/sendMessage'
database = {'host': 'localhost' if DEBUG else 'db', 'db': 'cnb'}

log_level = logging.DEBUG if DEBUG else logging.INFO
log_file = 'cnb_unitn.log'

scrape_timeout = 300 if DEBUG else 5 * 60  # seconds


old_news_factor = 2
