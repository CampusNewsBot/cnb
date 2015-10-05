import time
import logging
from logger import logger
from config import config
from schema import tables_creator
from sys import argv

def loop(scrapers):
    while True:
        instances = [scraper() for scraper in scrapers]
        logging.info('StartingLoop')
        for instance in instances:
            instance.update()
        time.sleep(config['refresh_rate'])

def scrape(scrapers):
    if 'initdb' in argv:
        tables_creator()
    else:
        loop(scrapers)
