import _thread
import time
import logging
import config
from initialize import create_db
from scrapers.implementations import scrapers
import telegram


def repeat(func, timeout):
    while True:
        func()
        time.sleep(timeout)

# Setup logging
logger = logging.getLogger()
logger.setLevel(config.log_level)
fileHandler = logging.FileHandler(config.log_file)
logger.addHandler(fileHandler)


# Create db if necessary
create_db()

# Start scraper threads
for scraper in scrapers:
    _thread.start_new_thread(repeat, (scraper.run, config.scrape_timeout))

# Start Telegram sender Thread
sender = telegram.Sender()
_thread.start_new_thread(sender.repeat)

while True:
    time.sleep(60)
