import json
import logging
from sys import argv
import bs4
import urllib2
import requests
import datetime
import peewee
from playhouse.shortcuts import model_to_dict
from schema import *
from serializer import date_serializer
from config import config

class Scraper():
    """
    Parent class for actual scrapers. Each scraper should define:
    - self.URL as the url to be scraped
    - self.parse as a function that takes a beautifulSoup object from self.html
      and parses it as a list of dictionaries to be placed in self.news using
      the following convention:
      {
        "author": the message author,
        "text": the message text,
        "date": a date formatted in RFC3339 representing the scraping time
      }
    """
    def __init__(self):
        self.DEPARTMENT = self.__class__.__name__[:-7].lower()
        self.html = ''
        self.raw = ''
        self.news = []
        self.config = config
        logging.info('InstanceCreated', extra={'department':self.DEPARTMENT})

    def fetch(self):
        logging.info('Fetching', extra={'department':self.DEPARTMENT})
        self.fetch_time = datetime.datetime.now()
        self.raw = urllib2.urlopen(self.URL).read()
        self.html_to_unicode()
        self.html = bs4.BeautifulSoup(self.raw, 'lxml')
        logging.info('Fetched')

    def html_to_unicode(self):
        lines = self.raw.split('\n')
        self.raw = ''
        for line in lines:
            if line:
                encoding = bs4.dammit.chardet.detect(line)
                self.raw += line.decode(encoding['encoding'])

    def parse(self):
        pass

    def parse_wrapper(self):
        self.news = []
        self.parse()
        self.news = self.news[::-1]
        logging.info('MessagesParsed', extra={'count':len(self.news),
                                              'department':self.DEPARTMENT})

    def sync(self):
        db.connect()
        department, _ = Department.get_or_create(name=self.DEPARTMENT)
        old_messages = list(Message.select().join(Author) \
                            .where(Author.department==department) \
                            .order_by(+Message.id).limit(len(self.news)*2))

        logging.debug('ComparingMessageLists')
        for message in old_messages:
            logging.debug('ComparingMessage',
                          extra={'old':message.text[:40],
                                 'new':self.news[0]['text'][:40]})
            if message.text == self.news[0]['text']:
                self.news.pop(0)
                logging.debug('Match')
            else:
                logging.debug('DoesNotMatch')

        for news_piece in self.news:
            author, _ = Author.get_or_create(department=department,
                                             name=news_piece['author'])

            message = Message.create(author=author, text=news_piece['text'])
            logging.debug('MessageSynced', extra={'id':message.id})
        db.close()
        logging.info('MessagesSynced', extra={'count':len(self.news)})

    def post(self):
        headers = {'X-Auth-Key':config['orchestrator']['keys'][self.DEPARTMENT],
                   'Content-Type':'application/json'}
        url = '{}/channel/{}-{}'.format(config['orchestrator']['host'],
                                           config['orchestrator']['base'],
                                           self.DEPARTMENT)
        db.connect()
        department = Department.get(name=self.DEPARTMENT)
        messages = list(Message.select().join(Author) \
                        .where(Author.department==department,
                               Message.receivers == -1))

        logging.info('SendingMessages', extra={'count':len(messages)})
        for message in messages:
            payload = model_to_dict(message)
            payload['author'] = payload['author']['name']
            payload = json.dumps(payload,default=date_serializer)
            if not '--stealth' in argv:
                response = requests.post(url=url, data=payload, headers=headers,
                                         verify=config['orchestrator']['valid_cert'])
                if response.status_code == 200:
                    message.receivers = response.json()['receivers']
                    message.save()
                    logging.debug('MessageSent',extra={'id':message.id,
                                                   'receivers':message.receivers
                                                   })
                else:
                    logging.error('OrchestratorHookDown',
                                  extra={'code':response.status_code,
                                         'message_id':message.id})
            else:
                message.receivers = 0
                message.save()
        db.close()

    def update(self):
        logging.info('StartUpdate', extra={'date':datetime.datetime.now()})
        try:
            self.fetch()
        except urllib2.URLError:
            logging.error('NewsFeedDown', extra={'url':self.URL})
            return
        except AttributeError:
            logging.error('ParsingFailed', extra={'url':self.URL})
            return
        self.parse_wrapper()
        try:
            self.sync()
        except peewee.OperationalError:
            logging.error('DBError')
            return
        try:
            self.post()
        except requests.exceptions.RequestException:
            logging.error('OrchestratorHookDown')
        except peewee.OperationalError:
            logging.error('DBError')
