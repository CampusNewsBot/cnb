import _thread
import time
import config
from initialize import create_db
from scrapers.implementations import scrapers
import telegram


def repeat(func, timeout):
    while True:
        func()
        time.sleep(timeout)

create_db()

for scraper in scrapers:
    _thread.start_new_thread(repeat, (scraper.run, config.scrape_timeout))

sender = telegram.Sender()
_thread.start_new_thread(repeat, (sender.send_messages, config.send_timeout))

while True:
    time.sleep(60)
