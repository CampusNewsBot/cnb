DEBUG = False
DEBUG_NO_SEND = False

database = {'host': 'localhost' if DEBUG else 'db', 'name': 'cnb'}
scrape_timeout = 20 if DEBUG else 5 * 60  # seconds

old_news_factor = 2
