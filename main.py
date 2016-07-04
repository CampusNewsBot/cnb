import _thread
from initialize import create_db
from scrapers.implementations import scrapers
from telegram import send_messages

create_db()

for scraper in scrapers:
    _thread.start_new_thread(scraper.run)

_thread.start_new_thread(send_messages)

while True:
    pass
