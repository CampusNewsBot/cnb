DEBUG = True
DEBUG_NO_SEND = False

telegram_url = 'https://api.telegram.org/bot{}/sendMessage'
database = {'host': 'localhost' if DEBUG else 'db', 'name': 'cnb'}

scrape_timeout = 20 if DEBUG else 5 * 60  # seconds
send_timeout = 10 if DEBUG else 1 * 60

old_news_factor = 2
