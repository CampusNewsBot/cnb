import _thread
import time
import config
from initialize import create_db
from scrapers.implementations import scrapers
from telegram import send_messages


def repeat(func, timeout):
    while True:
        func()
        time.sleep(timeout)

create_db()

for scraper in scrapers:
    _thread.start_new_thread(repeat, (scraper.run, config.scrape_timeout))

_thread.start_new_thread(send_messages, ())

while True:
    time.sleep(60)
