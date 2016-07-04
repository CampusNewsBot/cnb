import urllib
import logging
import bs4
import rethinkdb as r
import config


class Scraper:
    def __init__(self):
        # self.name = ''
        logging.info('Starting ', self.name)

        self.db = r.connect(host=config.database['host'],
                            db=config.database['name'])
        self.old_news_factor = config.old_news_factor

    def run(self):
        url = r.table('chats').get(self.name).run(self.db)['url']
        raw = self.fetch(url)
        candidate_news = self.parse(raw)
        actual_news = self.check(candidate_news)
        self.update(actual_news)

    def fetch(self, url):
        logging.debug('Fetching URL')
        return urllib.request.urlopen(url).read()

    def parse(self, raw):
        logging.debug('Parsing HTML')
        html = bs4.BeautifulSoup(raw, 'lxml')
        return self.news_parser(html)

    def check(self, candidate_news):
        logging.debug('Checking against existing news')
        old_news = r.table('news').filter({'chat': self.name})\
            .order_by('fetch_date')\
            .limit(self.old_news_factor * len(candidate_news))\
            .pluck('text').run(self.db)
        old_news = list(map(lambda x: x['text'], old_news))

        actual_news = []
        for candidate in candidate_news:
            logging.debug('Checking: ', candidate['text'][:20])
            if candidate['text'] not in old_news:
                actual_news.append(candidate)
        return actual_news

    def update(self, actual_news):
        logging.debug('Updating news')
        for news in actual_news:
            news.update({'chat': self.name, 'fetch_date': r.now(),
                         'send_date': None})
            r.table('news').insert(news).run(self.db)
