from scraper import Scraper
import logging
class DisiScraper(Scraper):
    URL = 'http://myuni.edu/news'

    def html_to_unicode(self):
        # a string is passed in self.raw
        # a string is expected in self.raw
        pass

    def parse(self):
        # a BeautifulSoup object is passed in self.html
        # a list of dictionaries is expected in self.news
        # in the following format:
        # {
        #     'author':'myAuthor',
        #     'text': 'myText'
        # }
        pass
