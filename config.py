import logging

DEBUG = False
DEBUG_NO_SEND = False

telegram_url = 'https://api.telegram.org/bot{}/sendMessage'
database = {'host': 'localhost' if DEBUG else 'db', 'db': 'cnb'}

log_level = logging.DEBUG if DEBUG else logging.INFO
log_file = 'cnb_unitn.log'

scrape_timeout = 20 if DEBUG else 5 * 60  # seconds
send_timeout = 10 if DEBUG else 1 * 60

# can send at most 3 messages every 5 * send_timeout seconds
send_limit_messages = 3
send_limit_intervals = 5

old_news_factor = 2
