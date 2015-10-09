import time
import logger
from config import config
from schema import tables_creator
from sys import argv

def loop(scrapers):
    instances = [scraper() for scraper in scrapers]
    while True:
        for instance in instances:
            instance.update()
        time.sleep(config['refresh_rate'])

def scrape(scrapers):
    if 'init' in argv:
        tables_creator()
    elif 'run' in argv:
        loop(scrapers)
