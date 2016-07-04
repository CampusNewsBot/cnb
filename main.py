import _thread
from telegram import send_messages
from scrapers.implementations import scrapers


for scraper in scrapers:
    _thread.start_new_thread(scraper.run)

_thread.start_new_thread(send_messages)

while True:
    pass
