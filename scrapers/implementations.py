import re
import logging
from .abstract import Scraper


class DisiScraper(Scraper):
    def __init__(self):
        self.regex = re.compile('.+ da (.*)')
        self.name = 'disi'
        super().__init__()

    def news_parser(self, html):
        news = []
        for tag in [n for n in html.find_all('a') if 'name' in n.attrs]:
            try:
                tag = tag.tr.td
                font_tags = tag.find_all('font')
                author_parsed = self.regex.match(font_tags[1].text).groups()
                news.append({
                    'author': author_parsed[0],
                    'text': font_tags[0].text,
                })

            except AttributeError:
                logging.warning('ParsingError', exc_info=True)
        return news[::-1]


class DicamScraper(Scraper):
    def __init__(self):
        self.regex = re.compile('(.+)inserito il .* da (.*)', re.DOTALL)
        self.name = 'dicam'
        super().__init__()

    def news_parser(self, html):
        news = []
        for row in self.html.table.find_all('td'):
            news_piece = {}
            matches = self.REGEX.match(row.text).groups()
            news_piece['text'], news_piece['author'] = matches
            news.append(news_piece)
        return self.news


class DiiCibioScraper(Scraper):
    def __init__(self):
        self.regex = re.compile(u'(.+)inserito il .* da (.*)', re.DOTALL)
        self.name = 'dii-cibio'
        super().__init__()

    def news_parser(self, html):
        news = []
        for row in self.html.find_all('table')[1].find_all('tr'):
            matches = self.regex.match(row.td.text).groups()
            news_piece = {}
            news_piece['text'], news_piece['author'] = matches
            news.append(news_piece)
        return news


class WebUnitnScraper(Scraper):
    def news_parser(self):
        news = []
        avvisi = self.html.find_all(class_='avviso')
        for avv in avvisi:
            testo = avv.find_all(class_='avvisoTesto')[0]
            news_piece = {
                'author': avv.find_all(class_='avvisoDocente')[0].a.text,
                'text': testo.a.text + '\n' + testo.a.attrs['href']
            }
            news.append(news_piece)
        return news

        # The following code would provide a more meaningful text
        # for each message, the caveat is a much higher number of requests
        # avv = avv.find_all(class_='avvisoTesto')[0]
        # html = urllib2.urlopen(avv.a.attrs['href']).read()
        # asoup = bs4.BeautifulSoup(html, 'lxml')
        # containers = asoup.find_all(class_='ui-widget-content')
        # for c in containers:
        #     print c
        #     if c.h3 and c.h3.text.find(avv.a.attrs['title']) != -1:
        #         news_piece['text'] = c.div.text
        #         self.news.append(news_piece)


class LettereScraper(WebUnitnScraper):
    name = 'lettere'


class GiurisprudenzaScraper(WebUnitnScraper):
    name = 'giurisprudenza'


class EconomiaScraper(WebUnitnScraper):
    name = 'economia'


class WebMagazineScraper(Scraper):
    def news_parser(self):
        view_content = self.html.find_all(class_='view-content')[0]
        items = view_content.find_all(class_='views-row')
        news = []

        for item in items:
            news_piece = {
                'author': 'dipartimento di {}'.format(self.DEPARTMENT),
                'text': item.a.text + '\n' + item.a.attrs['href']
            }
            news.append(news_piece)
        return self.news


class SociologiaScraper(WebMagazineScraper):
    name = 'sociologia'


class PsicologiaScraper(WebMagazineScraper):
    name = 'psicologia'

scrapers = [
    DisiScraper(),
    DiiCibioScraper(),
    DicamScraper(),
    LettereScraper(),
    GiurisprudenzaScraper(),
    EconomiaScraper(),
    SociologiaScraper(),
    PsicologiaScraper(),
]
