DEBUG = True
DEBUG_NO_SEND = True

database = {'host': 'localhost' if DEBUG else 'db', 'name': 'cnb'}
scrape_timeout = 20 if DEBUG else 5 * 60  # seconds
